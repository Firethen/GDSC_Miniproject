from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from app.models import db, Product,Purchase, Gonggu_product, Product_like, Market_like, Keyword,Keyword_market_link, Gonggu_group

zzim_bp = Blueprint('zzim', __name__)

# 이 하나의 URL에서 상품찜버튼을 누른것, 혹은 마켓찜 버튼을 누른것에 대한 request를 동시에 처리.(문제없죠?)
# 단순 찜 반영해서 DB업데이트하고, 바로 추천알고리즘을 실행시켜서 다음 리스트 띄울 때 반영하려고 합니다.
@zzim_bp.route('/product-details/zzim', methods=['POST'])
@login_required
def zzim():
    data = request.get_json()
    product_id = data.get('product_id')
    market_id = data.get('market_id')
    p_like = data.get('p_like')     #상품찜 의미(0이면 상품찜안누름, 1이면 상품찜 누름)
    m_like = data.get('m_like')     #마켓찜 의미(마찬가지)
    user_id = current_user.id
    if p_like == 1 and m_like ==0:
        gonggu_product = Gonggu_product.query.filter_by(market_id=market_id,product_id = product_id).first()
        gonggu_product_id = gonggu_product.id
        prod_like = Product_like.query.filter_by(customer_id=user_id, gonggu_product_id = gonggu_product_id).first()

        if prod_like is None:            # prod_like가 존재하지 않으면 새 행 추가(당연히 존재하지 않아야겠지)
            new_prod_like = Product_like(customer_id=user_id, gonggu_product_id=gonggu_product_id)
            db.session.add(new_prod_like)
            db.session.commit()
            return jsonify({'message': 'Product liked successfully'}), 201

    if p_like == 0 and m_like == 1:
        market_like = Market_like.query.filter_by(customer_id = user_id,market_id = market_id).first()
        if market_like is None:            # prod_like가 존재하지 않으면 새 행 추가(당연히 존재하지 않아야겠지)
            new_market_like = Market_like(customer_id=user_id, market_id = market_id)
            db.session.add(new_market_like)
            db.session.commit()
            return jsonify({'message': 'Market liked successfully'}), 201
        
    return jsonify({'message': 'Invalid request or nothing to delete'}), 400
        

#상품, 마켓찜을 삭제함(이미 찜인지 아닌지 여부는, /product-details 라우트에서 전달했어서 알수 있음)
@zzim_bp.route('/product-details/zzim_del', methods=['POST'])
@login_required
def zzim_del():
    data = request.get_json()
    product_id = data.get('product_id')
    market_id = data.get('market_id')
    p_like = data.get('p_like')     # p_like가 1이면 p_like를 삭제하겠다는 의미!!
    m_like = data.get('m_like')     # 마찬가지
    user_id = current_user.id

    # 상품 찜 제거
    if p_like == 1 and m_like == 0:
        gonggu_product = Gonggu_product.query.filter_by(market_id=market_id, product_id=product_id).first()
        if gonggu_product:
            gonggu_product_id = gonggu_product.id
            prod_like = Product_like.query.filter_by(customer_id=user_id, gonggu_product_id=gonggu_product_id).first()
            if prod_like:
                db.session.delete(prod_like)
                db.session.commit()
                return jsonify({'message': 'Product-like removed successfully'}), 200

    # 마켓 찜 제거
    if m_like == 1 and p_like == 0:
        market_like = Market_like.query.filter_by(customer_id=user_id, market_id=market_id).first()
        if market_like:
            db.session.delete(market_like)
            db.session.commit()
            return jsonify({'message': 'Market-like removed successfully'}), 200

    return jsonify({'message': 'Invalid request or nothing to delete'}), 400    