#상품에 대한 공동구매, 관심클릭에 대한 CRUD구현
from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from app.models import db, Product, Group, group_product

product_bp = Blueprint('product', __name__)

# 상품페이지에서 상품A에 대한 공동구매 그룹 -> http쿼리에서 상품A페이지에 대한 정보를 읽고 DB에서 탐색. 그리고 해당하는 그룹도 탐색
# 이후 해당 그룹테이블에 user추가, 이후 user테  이블에도 추가.
# 그리고 메인페이지로 리디렉션

#상품 리스트로 넘겨주기
'''> 유기농,로컬푸드, 상품사진도 넘겨야겠지? <'''
@product_bp.route('/products', methods=['GET'])
@login_required
def get_product():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            'name': product.name,
            'category': product.category
        }
        product_list.append(product_data)
    
    return jsonify(product_list)


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
