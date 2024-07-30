from flask import Blueprint, request, jsonify
import mysql.connector
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

recommend_bp = Blueprint('recommend', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host="gdsc-mini24.c58asus2kgn4.ap-northeast-2.rds.amazonaws.com",
        user="admin",
        password="k7rN%7)iSa%-L",
        database="gonggu",
        port=3306
    )

def fetch_data():
    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    cursor.execute("SELECT customer_id, gonggu_product_id FROM product_like")
    product_likes = cursor.fetchall()
    print(f"Product Likes: {len(product_likes)} records")

    cursor.execute("SELECT id AS gonggu_product_id, product_id, market_id, title FROM gonggu_product")
    gonggu_products = cursor.fetchall()
    print(f"Gonggu Products: {len(gonggu_products)} records")

    cursor.execute("SELECT customer_id, market_id FROM market_like")
    market_likes = cursor.fetchall()
    print(f"Market Likes: {len(market_likes)} records")

    cursor.execute("""
        SELECT kml.market_id, k.keyword 
        FROM keyword_market_link kml
        JOIN keyword k ON kml.keyword_id = k.id
    """)
    market_keywords = cursor.fetchall()
    print(f"Market Keywords: {len(market_keywords)} records")

    return product_likes, gonggu_products, market_likes, market_keywords

def prepare_data(product_likes, gonggu_products, market_likes, market_keywords):
    product_likes_df = pd.DataFrame(product_likes, columns=['customer_id', 'gonggu_product_id'])
    gonggu_products_df = pd.DataFrame(gonggu_products, columns=['gonggu_product_id', 'product_id', 'market_id', 'title'])
    market_likes_df = pd.DataFrame(market_likes, columns=['customer_id', 'market_id'])
    market_keywords_df = pd.DataFrame(market_keywords, columns=['market_id', 'keyword'])

    print(f"Product Likes DF: {product_likes_df.shape}")
    print(f"Gonggu Products DF: {gonggu_products_df.shape}")
    print(f"Market Likes DF: {market_likes_df.shape}")
    print(f"Market Keywords DF: {market_keywords_df.shape}")

    merged_df = pd.merge(product_likes_df, gonggu_products_df, on='gonggu_product_id')
    user_product_df = merged_df[['customer_id', 'product_id']].copy()
    user_product_df.loc[:, 'rating'] = 1

    if user_product_df.empty:
        print("User Product DataFrame is empty")
        return None, None, None

    market_likes_df = pd.merge(market_likes_df, market_keywords_df, on='market_id')
    market_keywords_count = market_likes_df.groupby(['customer_id', 'market_id', 'keyword']).size().reset_index(name='count')

    def calculate_keyword_weight(row):
        customer_id = row['customer_id']
        product_id = row['product_id']
        related_markets = gonggu_products_df[gonggu_products_df['product_id'] == product_id]['market_id'].unique()
        keyword_weights = market_keywords_count[(market_keywords_count['customer_id'] == customer_id) & (market_keywords_count['market_id'].isin(related_markets))]['count'].sum()
        return keyword_weights

    user_product_df.loc[:, 'keyword_weight'] = user_product_df.apply(calculate_keyword_weight, axis=1)
    user_product_df.loc[:, 'rating'] += user_product_df['keyword_weight']

    print(f"User Product DF: {user_product_df.shape}")
    print(user_product_df.head())

    reader = Reader(rating_scale=(0, user_product_df['rating'].max()))
    data = Dataset.load_from_df(user_product_df[['customer_id', 'product_id', 'rating']], reader)

    trainset, testset = train_test_split(data, test_size=0.25)
    algo = SVD()
    algo.fit(trainset)

    return algo, user_product_df, gonggu_products_df

def recommend_gonggu_products_ml(user_id, algo, user_product_df, gonggu_products_df, n=5):
    if user_product_df is None or user_id not in user_product_df['customer_id'].unique():
        return []

    all_product_ids = user_product_df['product_id'].unique()
    predictions = [algo.predict(user_id, product_id) for product_id in all_product_ids]
    top_n_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:n]
    
    print(f"Top N Predictions for User {user_id}: {top_n_predictions}")

    recommended_product_ids = [pred.iid for pred in top_n_predictions]

    recommended_gonggu_products = gonggu_products_df[gonggu_products_df['product_id'].isin(recommended_product_ids)]

    recommended_gonggu_product_details = recommended_gonggu_products[['gonggu_product_id', 'product_id', 'market_id', 'title']].to_dict(orient='records')

    return recommended_gonggu_product_details

@recommend_bp.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id', type=int)
    
    if user_id is None:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        product_likes, gonggu_products, market_likes, market_keywords = fetch_data()
        algo, user_product_df, gonggu_products_df = prepare_data(product_likes, gonggu_products, market_likes, market_keywords)
        
        if algo is None or user_product_df is None or gonggu_products_df is None:
            return jsonify({'error': 'Insufficient data for recommendations'}), 500
        
        recommended_products = recommend_gonggu_products_ml(user_id, algo, user_product_df, gonggu_products_df)

        return jsonify(recommended_products), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommend_bp.route('/api/gonggu_product/<int:product_id>', methods=['GET'])
def get_gonggu_product(product_id):
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT title, price FROM gonggu_product WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    db_connection.close()

    if product:
        return jsonify(product), 200
    else:
        return jsonify({'error': 'Product not found'}), 404
