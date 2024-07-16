#상품에 대한 공동구매, 관심클릭에 대한 CRUD구현
from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from app.models import db, Product, Group, group_product

product_bp = Blueprint('product', __name__)

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