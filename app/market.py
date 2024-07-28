from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import Market, Market_like, Keyword, Keyword_market_link

market_bp = Blueprint('market', __name__)

@market_bp.route('/markets', methods=['GET'])
def get_markets():
    markets = Market.query.all()
    market_list = []
    for market in markets:
        keywords = Keyword.query.join(Keyword_market_link).filter(Keyword_market_link.market_id == market.id).all()
        keyword_list = [keyword.keyword for keyword in keywords]
        market_list.append({
            "id": market.id,
            "name": market.name,
            "keywords": keyword_list
        })
    return jsonify(market_list)

@market_bp.route('/favorite-markets', methods=['GET'])
@login_required
def get_favorite_markets():
    user_id = current_user.id
    favorite_markets = Market_like.query.filter_by(customer_id=user_id).all()
    market_list = [{"id": market.market.id, "name": market.market.name} for market in favorite_markets]
    return jsonify(market_list)