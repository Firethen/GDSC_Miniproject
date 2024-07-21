#상품에 대한 공동구매, 관심클릭에 대한 CRUD구현
from flask import Blueprint, request, jsonify, abort, session
from flask_login import login_required, current_user
from app.models import db, Product, Group, User, Market, Region,Region_Market, Gonggu_product, Product_like, Market_like, Keyword,Keyword_market_link
import json

product_bp = Blueprint('product', __name__)

#상품 리스트로 넘겨주기(로그인된 user의 지역과 일치하는 상품들만)
@product_bp.route('/products', methods=['GET'])
@login_required 
def get_products():

    # 현재 로그인된 유저의 ID를 가져옵니다
    user_id = current_user.id
    
    # 유저의 지역 정보를 가져옵니다
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_region_id = user.region_id

    products = Product.query.all()
    product_list = []
    for product in products:
        #공구상품에서 가져옵니다.
        gonggu_products = Gonggu_product.query.filter_by(product_id=product.pid).all()
        for gonggu_product in gonggu_products:
            if not gonggu_product:
                continue
            market_id = gonggu_product.market_id
        
            #사용자의 지역에 일치하는 상품만 리스트로 반환
            regions = Region_Market.query.filter_by(market_id=market_id).all()
            matching_region = [region for region in regions if region.r_id == user_region_id]
            if matching_region:     #matching_region이 리스트긴하지만, len이 1이어야 할것.
                product_data = {
                    'id': product.pid,                  #상품id
                    'market_id' : market_id,            #해당 상품의 마켓id
                    'name': product.name,               #상품이름
                }
                product_list.append(product_data)
    return jsonify(product_list)

#바로 위의 상품리스트에서 가지고있던 상품id 마켓id 바탕으로 <마켓이름 전달, (상품찜,마켓찜) 여부, 마켓의 키워드>를 return해주겠음.
@product_bp.route('/product-details', methods=['POST'])
@login_required
def get_product_details():
    data = request.get_json()
    product_id = data.get('product_id')
    market_id = data.get('market_id')
    p_like,m_like = False

    market = Market.query.filter_by(market_id=market_id).first()
    market_name = market.market_name

    user_id = current_user.id
    prod_like = Product_like.query.filter_by(customer_id=user_id,product_id=product_id).first()
    if prod_like:
        p_like = True
    mark_like = Market_like.query.filter_by(customer_id=user_id,market_id=market_id).first()
    if mark_like:
        m_like = True
    #keyword_ids를 사용하여 Keyword 테이블에서 해당 키워드 이름들을 조회
    keywords = Keyword.query.filter(Keyword.id.in_(keyword_ids)).all()
    #조회된 키워드 이름들을 리스트로 변환
    keyword_names = [keyword.keyword_name for keyword in keywords]
    
    keyword_links = Keyword_market_link.query.filter_by(market_id=market_id).all()
    keyword_ids = [link.keyword_id for link in keyword_links]
    return_data = {
            'product_id': product_id,
            'market_id': market_id,
            'market_name': market_name,
            'product_like': p_like,             #상품 찜 여부(True,False로 나타냄)
            'market_like': m_like,              #마켓 찜 여부
            'keyword_names': keyword_names      # 키워드 이름이 리스트형태
    }
    return jsonify(return_data)

# 그룹 참여 라우트
@product_bp.route('/products/<int:product_id>/join_group', methods=['POST'])
@login_required
def join_group():
    data = request.get_json()
    group_id = data.get('group_id')

    if not group_id:
        return jsonify({'error': 'Group ID is required'}), 400

    group = Group.query.filter_by(gid=group_id).first()
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    # 세션에 그룹 ID 저장 (장바구니 기능)
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(group_id)

    return jsonify({'group_id': group_id}), 200

