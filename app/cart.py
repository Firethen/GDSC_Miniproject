from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from app.models import db, Group, product, market

cart_bp = Blueprint('cart', __name__)


#Retrieve cart items
@cart_bp.route('/cart', methods=['GET'])
@login_required
def get_cart():
    cart = session.get('cart', [])
    groups = Group.query.filter(Group.gid.in_(cart)).all()
    group_list = []
    for group in groups:
        prod = product.query.filter_by(pid=group.product_id).first()
        mark = market.query.filter_by(mid=group.market_id).first()
        group_data = {
            'group_id': group.gid,
            '상품 이름': prod.name,
            '마켓 이름': mark.market_name,
            '최대 규모': group.grup_size,
            '현재 규모': group.current_size
        }
        group_list.append(group_data)

    return jsonify(group_list), 200
