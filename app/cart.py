from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from app.models import db, Product, Group, User, Market, Region,Region_Market,Purchase, Gonggu_product, Product_like, Market_like, Keyword,Keyword_market_link, Gonggu_group
import json
cart_bp = Blueprint('cart', __name__)


#Retrieve cart items
@cart_bp.route('/cart', methods=['GET'])
@login_required
def get_cart():
    cart = session.get('cart', [])
    groups = Gonggu_group.query.filter(Gonggu_group.id.in_(cart)).all()
    group_list = []
    for group in groups:
        prod = Gonggu_product.query.filter_by(id=group.gonggu_product_id).first()
        group_data = {
            'group_id'  : group.id,
            'market_id' : prod.market_id,
            'product_id': prod.product_id,
            'price'     : prod.price,       #가격
            'group_size': group.size
        }
        group_list.append(group_data)

    return jsonify(group_list), 200

# 장바구니 페이지에서 최종구매 버튼 클릭(POST, UPDATE(해당 그룹의 인원수 업데이트))
# => 구매개수도 requeset로 받고, 해당 세션에서는 그 항목삭제되고, DB에 주문테이블에 추가, 그룹테이블에 업데이트 처리.

@cart_bp.route('/cart/purchase', methods=['POST'])
@login_required
def group_purchase():
    # 요청에서 구매 수량을 가져옴
    data = request.get_json()
    purchase_quantity = data.get('구매수량')
    group_id = data.get('group_id')

    # 구매 수량이 유효한지 확인
    purchase_quantity = int(purchase_quantity)
    if not purchase_quantity or purchase_quantity<=0:
        return jsonify({'error': 'Invalid purchase quantity'}), 400

    # 그룹을 DB에서 찾습니다.
    group = Gonggu_group.query.filter_by(id=group_id).first()
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    '''if group.current_size + purchase_quantity > group.max_size:
        return jsonify({'error': 'Purchase exceeds group size limit'}), 400'''
    
    # 현재 규모를 증가시킵니다.
    group.size += 1
    db.session.commit()

    # 'purchase' 테이블에 주문 정보를 추가합니다.
    order = Purchase(customer_id=current_user.id, gonggu_group_id=group_id)
    db.session.add(order)
    db.session.commit()

    # 세션에서 장바구니 정보를 제거합니다.
    if 'cart' in session:
        if group_id in session['cart']:
            session['cart'].remove(group_id)
            if not session['cart']:
                session.pop('cart', None)

    return jsonify({'message': 'Purchase successful'}), 200
    