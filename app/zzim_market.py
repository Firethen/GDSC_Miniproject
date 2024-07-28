from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Market_like, Market

market_like_bp = Blueprint('market_like', __name__)

@market_like_bp.route('/market-like', methods=['POST'])
@login_required
def add_market_like():
    data = request.get_json()
    market_id = data.get('market_id')

    if not market_id:
        return jsonify({'message': 'Market ID is required'}), 400

    user_id = current_user.id
    market_like = Market_like.query.filter_by(customer_id=user_id, market_id=market_id).first()

    if market_like is None:
        new_market_like = Market_like(customer_id=user_id, market_id=market_id)
        db.session.add(new_market_like)
        db.session.commit()
        return jsonify({'message': 'Market liked successfully'}), 201

    return jsonify({'message': 'Market is already liked'}), 200

@market_like_bp.route('/market-like', methods=['DELETE'])
@login_required
def delete_market_like():
    data = request.get_json()
    market_id = data.get('market_id')

    if not market_id:
        return jsonify({'message': 'Market ID is required'}), 400

    user_id = current_user.id
    market_like = Market_like.query.filter_by(customer_id=user_id, market_id=market_id).first()

    if market_like:
        db.session.delete(market_like)
        db.session.commit()
        return jsonify({'message': 'Market like removed successfully'}), 200

    return jsonify({'message': 'Market like does not exist'}), 400

@market_like_bp.route('/favorite-markets', methods=['GET'])
@login_required
def get_favorite_markets():
    user_id = current_user.id
    favorite_markets = Market_like.query.filter_by(customer_id=user_id).all()
    
    market_list = []
    for favorite in favorite_markets:
        market = Market.query.get(favorite.market_id)
        if market:
            market_list.append({
                'id': market.id,
                'name': market.name
            })
    
    return jsonify(market_list), 200
