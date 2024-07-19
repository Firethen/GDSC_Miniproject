#상품에 대한 공동구매, 관심클릭에 대한 CRUD구현
from flask import Blueprint, request, jsonify, abort, session
from flask_login import login_required, current_user
from app.models import db, Product, Group, User, market
import json

product_bp = Blueprint('product', __name__)

#상품 리스트로 넘겨주기
@product_bp.route('/products', methods=['GET'])
@login_required
def get_products():

    # 현재 로그인된 유저의 ID를 가져옵니다
    user_id = current_user.id
    
    # 유저의 지역 정보를 가져옵니다
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_residence_area = user.residence_area

    products = Product.query.all()
    product_list = []
    for product in products:
        # 상품의 마켓 정보를 가져옵니다
        market_info = market.query.filter_by(market_id=product.market_id).first()
        if not market_info:
            continue
        
        # 마켓의 판매 지역을 가져옵니다
        sale_area = market_info.sale_area

        if isinstance(sale_area, str):
            sale_area = json.loads(sale_area)  # JSON 문자열을 파이썬 리스트로 변환
        
        # 유저의 지역이 판매 지역에 포함되는지 확인합니다
        if user_residence_area in sale_area:
            product_data = {
                'id': product.pid,
                'market_id' : product.market_id,
                'name': product.name,
                'category': product.category,
                'local_food' : product.local_food,
                'image_url' : product.image_url
            }
            product_list.append(product_data)
    
    return jsonify(product_list)

@product_bp.route('/products/<int:product_id>', methods=['GET'])
@login_required
def get_product_detail(product_id):
    product = Product.query.filter_by(pid=product_id).first() #url라우트의 해당 product_id에 해당하는 pid의 정보를 전달
    if product:
        product_data = {
            'id': product.pid,
            'market_id': product.market_id,
            'name': product.name,
            'category': product.category,
            'local_food': product.local_food,
            'image_url': product.image_url
        }
        return jsonify(product_data)
    else:
        return jsonify({'error': 'Product not found'}), 404

# 그룹 참여 라우트
@product_bp.route('/join_group', methods=['POST'])
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

# 장바구니페이지 클릭(GET)
# => user의 세션에 저장되어 있는 장바구니 공동구매그룹들을 return

# 장바구니 페이지에서 최종구매 버튼 클릭(POST, UPDATE(해당 그룹의 인원수 업데이트))
# => 구매개수도 requeset로 받고, 해당 세션에서는 그 항목삭제되고, DB에 주문테이블에 추가, 그룹테이블에 업데이트 처리.



@product_bp.route('/products/detail', methods=['POST'])
@login_required
def purchase_join_group():  #공동구매 그룹에 join
    


#~~~~~~~~~~~~~~~~~~~~~~~~수정필요~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
@product_bp.route('/product/<int:product_id>/join_group', methods=['POST'])
@login_required
def join_group(product_id):
    product = Product.query.get(gid)

    if not product:
        abort(404, description="Product not found")

    # 현재 유저를 해당 상품의 그룹에 추가
    if current_user not in product.groups:
        product.groups.append(current_user)
        db.session.commit()

    # 클라이언트에게 응답으로 전달할 데이터 구성
    response_data = {
        'message': 'You joined the group for this product successfully',
        'product_id': product.id,
        'user_id': current_user.id
    }

    return jsonify(response_data), 200
