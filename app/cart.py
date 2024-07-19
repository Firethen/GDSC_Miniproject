from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from app.models import db, Group, Product, Market,Order

cart_bp = Blueprint('cart', __name__)


#Retrieve cart items
@cart_bp.route('/cart', methods=['GET'])
@login_required
def get_cart():
    cart = session.get('cart', [])
    groups = Group.query.filter(Group.gid.in_(cart)).all()
    group_list = []
    for group in groups:
        prod = Product.query.filter_by(pid=group.product_id).first()
        mark = Market.query.filter_by(mid=group.market_id).first()
        group_data = {
            'group_id': group.gid,
            '상품 이름': prod.name,
            '마켓 이름': mark.market_name,
            '최대 규모': group.grup_size,
            '현재 규모': group.current_size
        }
        group_list.append(group_data)

    return jsonify(group_list), 200

# 장바구니 페이지에서 최종구매 버튼 클릭(POST, UPDATE(해당 그룹의 인원수 업데이트))
# => 구매개수도 requeset로 받고, 해당 세션에서는 그 항목삭제되고, DB에 주문테이블에 추가, 그룹테이블에 업데이트 처리.

@cart_bp.route('/cart/<int:group_id>/purchase', methods=['POST'])
@login_required
def purchase(group_id):
    # 요청에서 구매 수량을 가져옴
    data = request.get_json()
    purchase_quantity = data.get('구매수량')

    # 구매 수량이 유효한지 확인
    if not purchase_quantity or purchase_quantity<=0:
        return jsonify({'error': 'Invalid purchase quantity'}), 400

    # 그룹을 데이터베이스에서 찾습니다.
    group = Group.query.filter_by(gid=group_id).first()
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    if group.current_size + purchase_quantity > group.max_size:
        return jsonify({'error': 'Purchase exceeds group size limit'}), 400
    
    # 현재 규모를 증가시킵니다.
    group.current_size += purchase_quantity
    db.session.commit()

    # 'order' 테이블에 주문 정보를 추가합니다.
    order = Order(user_id=current_user.id, gid=group_id, quantity=purchase_quantity)
    db.session.add(order)
    db.session.commit()

    # 세션에서 장바구니 정보를 제거합니다.
    if 'cart' in session:
        if group_id in session['cart']:
            session['cart'].remove(group_id)
            if not session['cart']:
                session.pop('cart', None)

    return jsonify({'message': 'Purchase successful'}), 200
    