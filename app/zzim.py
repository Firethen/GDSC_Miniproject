from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from app.models import db, Gonggu_product, Product_like, Market_like

zzim_bp = Blueprint('zzim', __name__)

@zzim_bp.route('/product-details/zzim', methods=['POST'])
@login_required
def zzim():
    data = request.get_json()
    print(f"Received data: {data}")
    market_id = data.get('market_id')
    p_like = int(data.get('p_like'))
    m_like = int(data.get('m_like'))
    user_id = current_user.id

    if p_like == 1 and m_like == 0:
        gonggu_product = Gonggu_product.query.filter_by(market_id=market_id).first()
        if gonggu_product:
            gonggu_product_id = gonggu_product.id
            prod_like = Product_like.query.filter_by(customer_id=user_id, gonggu_product_id=gonggu_product_id).first()
            if prod_like is None:
                new_prod_like = Product_like(customer_id=user_id, gonggu_product_id=gonggu_product_id)
                db.session.add(new_prod_like)
                db.session.commit()
                return jsonify({'message': 'Product liked successfully'}), 201

    if p_like == 0 and m_like == 1:
        market_like = Market_like.query.filter_by(customer_id=user_id, market_id=market_id).first()
        if market_like is None:
            new_market_like = Market_like(customer_id=user_id, market_id=market_id)
            db.session.add(new_market_like)
            db.session.commit()
            return jsonify({'message': 'Market liked successfully'}), 201

    return jsonify({'message': 'Invalid request or nothing to delete'}), 400

@zzim_bp.route('/product-details/zzim_del', methods=['POST'])
@login_required
def zzim_del():
    data = request.get_json()
    print(f"Received data for deletion: {data}")
    market_id = data.get('market_id')
    p_like = int(data.get('p_like'))
    m_like = int(data.get('m_like'))
    user_id = current_user.id

    if p_like == 1 and m_like == 0:
        gonggu_product = Gonggu_product.query.filter_by(market_id=market_id).first()
        if gonggu_product:
            gonggu_product_id = gonggu_product.id
            prod_like = Product_like.query.filter_by(customer_id=user_id, gonggu_product_id=gonggu_product_id).first()
            if prod_like:
                db.session.delete(prod_like)
                db.session.commit()
                return jsonify({'message': 'Product-like removed successfully'}), 200

    if m_like == 1 and p_like == 0:
        market_like = Market_like.query.filter_by(customer_id=user_id, market_id=market_id).first()
        if market_like:
            db.session.delete(market_like)
            db.session.commit()
            return jsonify({'message': 'Market-like removed successfully'}), 200

    return jsonify({'message': 'Invalid request or nothing to delete'}), 400
