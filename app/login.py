from flask import Blueprint, request, jsonify, abort, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('ID')
        password = data.get('password')

        if not user_id or not password:
            abort(400, description="Missing ID or password")

        user = User.query.filter_by(id=user_id).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'message': 'Logged in successfully'}), 200
        else:
            abort(401, description="Invalid credentials")
    abort(405)  # POST 요청 외의 메서드는 허용하지 않음

@login_bp.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        ID = data.get('ID')
        username = data.get('username')
        phone_num = data.get('phone_num')
        residence_area = data.get('residence_area')
        password = data.get('password')

        if not ID or not username or not phone_num or not residence_area or not password:
            abort(400, description="Missing required fields")

        existing_user = User.query.filter_by(id=ID).first()
        if existing_user:
            abort(400, description="User already exists")

        user = User(id=ID, username=username, phone_num=phone_num, residence_area=residence_area)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Account created successfully'}), 201

    abort(405)  # GET 요청은 허용하지 않음

@login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200

    abort(405)  # GET 요청은 허용하지 않음
