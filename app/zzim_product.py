from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Product_like, Gonggu_product

zzim_product_bp = Blueprint('zzim_product', __name__, url_prefix='/api')

@zzim_product_bp.route('/product-like', methods=['POST'])
@login_required
def add_product_like():
    data = request.get_json()
    gonggu_product_id = data.get('gonggu_product_id')

    if not gonggu_product_id:
        return jsonify({'message': 'Product ID is required'}), 400

    user_id = current_user.id
    product_like = Product_like.query.filter_by(customer_id=user_id, gonggu_product_id=gonggu_product_id).first()

    if product_like is None:
        new_product_like = Product_like(customer_id=user_id, gonggu_product_id=gonggu_product_id)
        db.session.add(new_product_like)
        db.session.commit()
        return jsonify({'message': 'Product liked successfully'}), 201

    return jsonify({'message': 'Product is already liked'}), 200

@zzim_product_bp.route('/product-like', methods=['DELETE'])
@login_required
def delete_product_like():
    data = request.get_json()
    gonggu_product_id = data.get('gonggu_product_id')

    if not gonggu_product_id:
        return jsonify({'message': 'Product ID is required'}), 400

    user_id = current_user.id
    product_like = Product_like.query.filter_by(customer_id=user_id, gonggu_product_id=gonggu_product_id).first()

    if product_like:
        db.session.delete(product_like)
        db.session.commit()
        return jsonify({'message': 'Product like removed successfully'}), 200

    return jsonify({'message': 'Product like does not exist'}), 400

@zzim_product_bp.route('/favorite-products', methods=['GET'])
@login_required
def get_favorite_products():
    user_id = current_user.id
    favorite_products = Product_like.query.filter_by(customer_id=user_id).all()

    product_list = []
    for favorite in favorite_products:
        gonggu_product = Gonggu_product.query.filter_by(product_id=favorite.gonggu_product_id).first()
        if gonggu_product:
            product_list.append({
                'id': gonggu_product.product_id,
                'name': gonggu_product.title,
                'price': gonggu_product.price
            })
    
    return jsonify(product_list), 200