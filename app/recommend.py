import mysql.connector
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

try:
    # MySQL 데이터베이스에 연결
    db_connection = mysql.connector.connect(
        host="gdsc-mini24.c58asus2kgn4.ap-northeast-2.rds.amazonaws.com",
        user="admin",
        password="k7rN%7)iSa%-L",
        database="gonggu",
        port=3306 
    )

    cursor = db_connection.cursor()

    print("Database connection successful!")

except mysql.connector.Error as err:
    print(f"Error: {err}")

# product_like 테이블
cursor.execute("""
    SELECT customer_id, gonggu_product_id 
    FROM product_like
""")
product_likes = cursor.fetchall()

# gonggu_product 테이블
cursor.execute("""
    SELECT id AS gonggu_product_id, product_id, market_id
    FROM gonggu_product
""")
gonggu_products = cursor.fetchall()

# market_like 테이블
cursor.execute("""
    SELECT customer_id, market_id 
    FROM market_like
""")
market_likes = cursor.fetchall()

# keyword_market_link 테이블
cursor.execute("""
    SELECT kml.market_id, k.keyword 
    FROM keyword_market_link kml
    JOIN keyword k ON kml.keyword_id = k.id
""")
market_keywords = cursor.fetchall()

# 데이터프레임으로 변환
product_likes_df = pd.DataFrame(product_likes, columns=['customer_id', 'gonggu_product_id'])
gonggu_products_df = pd.DataFrame(gonggu_products, columns=['gonggu_product_id', 'product_id', 'market_id'])
market_likes_df = pd.DataFrame(market_likes, columns=['customer_id', 'market_id'])
market_keywords_df = pd.DataFrame(market_keywords, columns=['market_id', 'keyword'])

# 실제 상품 ID로 매핑하여 사용자-상품 데이터프레임 생성
merged_df = pd.merge(product_likes_df, gonggu_products_df, on='gonggu_product_id')
user_product_df = merged_df[['customer_id', 'product_id']].copy()
user_product_df.loc[:, 'rating'] = 1

# 사용자가 찜한 마켓의 키워드에 기반한 가중치 계산
market_likes_df = pd.merge(market_likes_df, market_keywords_df, on='market_id')
market_keywords_count = market_likes_df.groupby(['customer_id', 'market_id', 'keyword']).size().reset_index(name='count')

def calculate_keyword_weight(row):
    customer_id = row['customer_id']
    product_id = row['product_id']
    related_markets = gonggu_products_df[gonggu_products_df['product_id'] == product_id]['market_id'].unique()
    keyword_weights = market_keywords_count[(market_keywords_count['customer_id'] == customer_id) & (market_keywords_count['market_id'].isin(related_markets))]['count'].sum()
    return keyword_weights

user_product_df.loc[:, 'keyword_weight'] = user_product_df.apply(calculate_keyword_weight, axis=1)
user_product_df.loc[:, 'rating'] += user_product_df['keyword_weight'] # 키워드 가중치도 반영

# surprise용 데이터셋 생성
reader = Reader(rating_scale=(0, user_product_df['rating'].max()))
data = Dataset.load_from_df(user_product_df[['customer_id', 'product_id', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=0.25)
algo = SVD()
algo.fit(trainset)

predictions = algo.test(testset)
rmse_value = accuracy.rmse(predictions)
print("RMSE:", rmse_value)

def recommend_gonggu_products_ml(user_id, n=5):
    all_product_ids = user_product_df['product_id'].unique()
    predictions = [algo.predict(user_id, product_id) for product_id in all_product_ids]
    top_n_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:n]
    recommended_product_ids = [pred.iid for pred in top_n_predictions]
    
    # 추천된 상품 ID에 해당하는 공동구매 상품 찾기
    recommended_gonggu_products = gonggu_products_df[gonggu_products_df['product_id'].isin(recommended_product_ids)]
    recommended_gonggu_product_ids = recommended_gonggu_products['gonggu_product_id'].unique()[:n]
    
    return recommended_gonggu_product_ids

# 사용자 1에게 추천할 공동구매 상품
user_id = 1
recommended_gonggu_products = recommend_gonggu_products_ml(user_id)
print("Recommended Gonggu Products for User 1:", recommended_gonggu_products)