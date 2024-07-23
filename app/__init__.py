from flask import Flask, redirect, url_for, jsonify
from flask_login import LoginManager
from sqlalchemy import text
from app.models import db, User
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

# Flask 애플리케이션을 생성하는 팩토리 함수
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY

    #SQLAlchemy 초기화
    db.init_app(app)

    #LoginManager 초기화
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # 로그인 페이지의 뷰 함수 이름

    # 로그인되지않은 사용자가 로그인필요 페이지 접근할 때 핸들링
    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('login'))

    @login_manager.user_loader
    def load_user(user_id):
        # Return the user object for the given user_id
        return User.query.get(int(user_id))

    # Blueprint import
    from app.login import login_bp
    from app.product import product_bp
    from app.cart import cart_bp

    # Blueprint 등록
    app.register_blueprint(login_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)

    @app.route('/test_db')
    def test_db():
        try:
            db.session.execute(text('SELECT 1'))
            return jsonify({"message": "Database connection successful"}), 200
        except Exception as e:
            return jsonify({"message": "Database connection failed", "error": str(e)}), 500

    #데이터베이스 생성
    with app.app_context():
        db.create_all()


    return app
