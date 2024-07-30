#상품에 대한 공동구매, 관심클릭에 대한 CRUD구현
from flask import Blueprint, request, jsonify, abort, session
from flask_login import login_required, current_user
<<<<<<< HEAD
from app.models import db, Product, User, Market, Region, Region_Market, Gonggu_product, Product_like, Market_like, Keyword,Keyword_market_link, Gonggu_group, Purchase
=======
from app.recommend import recommend_gonggu_products_ml
from app.models import db, Product, User, Market, Region,Region_Market, Gonggu_product, Product_like, Market_like, Keyword,Keyword_market_link, Gonggu_group
>>>>>>> f2e6c25e19dba7bb62b58c9d609158b68a221737
import json

product_bp = Blueprint('product', __name__)

#상품 리스트로 넘겨주기
@product_bp.route('/products', methods=['GET'])
@login_required
def get_products():
    # 현재 로그인된 유저의 ID를 가져옵니다
    user_id = current_user.id
    '''# 유저의 지역 정보를 가져옵니다
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_region_id = user.region_id'''

    #추천알고리즘 적용
    recommended_gonggu_products = recommend_gonggu_products_ml(user_id)
    recommended_products = Gonggu_product.query.filter(Gonggu_product.id.in_(recommended_gonggu_products)).all()
    product_list = []
    for r_p in recommended_products:
        product_data = {
            'id': r_p.product_id,                  #상품id
            'market_id' : r_p.market_id,           #해당 상품의 마켓id
            'name': r_p.title,                     #상품타이틀
        }
        product_list.append(product_data)
    return jsonify(product_list)
    '''products = Product.query.all()
    product_list = []
    for product in products:
        #공구상품에서 가져옵니다.
        gonggu_products = Gonggu_product.query.filter_by(product_id=product.id).all()
        for gonggu_product in gonggu_products:
            if not gonggu_product:
                continue
            market_id = gonggu_product.market_id
        
            #사용자의 지역에 일치하는 상품만 리스트로 반환
            regions = Region_Market.query.filter_by(market_id=market_id).all()
            matching_region = [region for region in regions if region.id == user_region_id]
            if matching_region:     #matching_region이 리스트긴하지만, len이 1이어야 할것.
                product_data = {
                    'id': product.id,                  #상품id
                    'market_id' : market_id,            #해당 상품의 마켓id
                    'name': product.name,               #상품이름
                }
                product_list.append(product_data)
    return jsonify(product_list)'''


#바로 위의 상품리스트에서 가지고있던 상품id 마켓id 바탕으로 <공구상품id, 가격, 그리고 각 그룹들id와 인원, 마켓이름 전달, (상품찜,마켓찜) 여부, 마켓의 키워드>를 return해주겠음.
@product_bp.route('/product-details', methods=['POST'])
@login_required
def get_product_details():
    data = request.get_json()
    product_id = data.get('product_id')
    market_id = data.get('market_id')
    p_like = False
    m_like = True

    #공구상품id, 가격,타이틀 찾기
    gonggu_product = Gonggu_product.query.filter_by(market_id=market_id,product_id = product_id).first()
    gonggu_product_id = gonggu_product.id
    gonggu_product_price = gonggu_product.price
    gonggu_product_title = gonggu_product.title
    
    #공구 상품id에 따른 공구 그룹들과 그룹size를 쌍으로 리스트화
    gonggu_groups = Gonggu_group.query.filter_by(gonggu_product_id=gonggu_product_id).all()
    group_list = []
    for group in gonggu_groups:
        group_data = {
            'id': group.id,
            'size': group.size
        }
        group_list.append(group_data)
        
    #마켓이름 찾기
    market = Market.query.filter_by(id=market_id).first()
    market_name = market.name

    #사용자가 마켓,상품찜한지 여부찾기
    user_id = current_user.id
    prod_like = Product_like.query.filter_by(customer_id=user_id,gonggu_product_id=product_id).first()
    if prod_like:
        p_like = True
    mark_like = Market_like.query.filter_by(customer_id=user_id,market_id=market_id).first()
    if mark_like:
        m_like = True
    
    keyword_links = Keyword_market_link.query.filter_by(market_id=market_id).all()
    keyword_ids = [link.keyword_id for link in keyword_links]
    
    keywords = Keyword.query.filter(Keyword.id.in_(keyword_ids)).all()
    keyword_names = [keyword.keyword for keyword in keywords]

    return_data = {
            'product_id': product_id,
            'market_id': market_id,
            'market_name': market_name,
            'title' : gonggu_product_title,
            'product_like': p_like,             #상품 찜 여부(True,False로 나타냄)
            'market_like': m_like,              #마켓 찜 여부
            'keyword_names': keyword_names,      # 키워드 이름이 리스트형태
            'price': gonggu_product_price,
            'groups': group_list                #공구그룹id와 각 size가 쌍(dict)으로 존재하는 리스트.
    }
    return jsonify(return_data)

@product_bp.route('/all-products', methods=['GET'])
def get_all_gonggu_products():
    gonggu_products = Gonggu_product.query.all()
    
    gonggu_product_list = []
    for gonggu_product in gonggu_products:
        product = Product.query.filter_by(id=gonggu_product.product_id).first()
        if not product:
            continue

        market = Market.query.filter_by(id=gonggu_product.market_id).first()
        market_name = market.name if market else 'Unknown'

        gonggu_product_data = {
            'gonggu_product_id': gonggu_product.id,
            'product_id': product.id,
            'market_id': gonggu_product.market_id,
            'name': product.name,
            'price': gonggu_product.price,
            'title': gonggu_product.title,
            'market_name': market_name
        }
        gonggu_product_list.append(gonggu_product_data)
    
    return jsonify(gonggu_product_list)


# 그룹 참여 라우트
@product_bp.route('/product-details/group', methods=['POST'])
@login_required
def join_group():
    data = request.get_json()
    group_id = data.get('group_id')
    if not group_id:
        return jsonify({'error': 'Group ID is required'}), 400

    group = Gonggu_group.query.filter_by(id=group_id).first()
    if not group:
        return jsonify({'error': 'Gonggu_group not found'}), 404
    
    # 세션에 그룹 ID 저장 (장바구니 기능)
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(group_id)

    return jsonify({'group_id': group_id}), 200


#사용자가 공동구매그룹을 새로 [생성]할 때
@product_bp.route('/product-details/group/make', methods=['POST'])
@login_required
def make_group():
    try:
        data = request.get_json()
        gonggu_product_id = data.get('gonggu_product_id')   # 공동구매상품테이블의 키(id)
        max_size = data.get('max_size')                     # 생성하려는 그룹의 최대 사이즈.

        #이미 존재하는 그룹들을 가져옴
        existing_groups = Gonggu_group.query.filter_by(gonggu_product_id=gonggu_product_id).all()
        # 기존 그룹들의 size 값 리스트
        existing_sizes = [group.size for group in existing_groups]
        # max_size가 기존 그룹들의 size ± 1 범위 내에 있는지 확인
        for size in existing_sizes:
            if abs(size - max_size) <= 1:
                return jsonify({'status': 'error', 'message': 'max_size가 기존재하는 그룹들의 size범위내에 있습니다.'}), 400

        new_group = Gonggu_group(gonggu_product_id = gonggu_product_id,size = max_size)
        db.session.add(new_group)
        db.session.commit()
        
        return jsonify({'status': 'success', 'group_id': new_group.id}), 201
    except Exception as e:      #예외 발생시 롤백(트랜잭션 관리)
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


##추가
@product_bp.route('/purchase', methods=['POST'])
@login_required
def purchase_product():
    data = request.get_json()

    customer_id = current_user.id  # 현재 로그인된 사용자 ID
    quantity = data.get('quantity')
    product_id = data.get('product_id')  # 사용자가 제공하는 Product ID
    gonggu_group_id = data.get('gonggu_group_id', 1)  # Optional

    if not quantity or not product_id:
        return jsonify({'message': 'Quantity and Product ID are required'}), 400

    # Product ID로 Gonggu_product 찾기
    gonggu_product = Gonggu_product.query.filter_by(product_id=product_id).first()
    if not gonggu_product:
        return jsonify({'message': 'Gonggu product not found'}), 404

    try:
        purchase = Purchase(
            customer_id=customer_id,
            gonggu_group_id=gonggu_group_id,  # Optional
            quantity=quantity,
            gonggu_product_id=gonggu_product.id  # 찾은 Gonggu_product의 ID 사용
        )
        db.session.add(purchase)
        db.session.commit()
        return jsonify({'message': 'Purchase completed successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
