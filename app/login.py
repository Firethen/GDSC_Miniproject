from flask import Blueprint, request, jsonify, abort, json
from flask_login import login_user, logout_user, login_required
from app.models import db, User, Region

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        ID = data.get('ID')
        password = data.get('password')

        if not ID or not password:
            abort(400, description="Missing ID or password")

        user = User.query.filter_by(identification=ID).first()
        if user and user.check_password(password):
            login_user(user)
            region = Region.query.filter_by(r_id=user.region_id).first()
            user_info = {
                'ID': user.id, #여기서 ID는 DB-customer의 PK ID를 의미.(identification이랑 다름)
                'User ID' : user.identification, #이거는 실제로 유저가 입력하는 ID
                'username': user.username,
                'region_name': region.dong_name, #지역 ID가 아니라 지역의 이름을 return
                'address' : user.address,
                'phone' : user.phone
            }
            return jsonify(user_info), 200
        else:
            abort(401, description="Invalid credentials")
    abort(405)  # POST 요청 외의 메서드는 허용하지 않음 

@login_bp.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        identification = data.get('identification')
        ID = data.get('id') 
        username = data.get('username')
        dong_name = data.get('dong_name')
        password = data.get('password')
        address = data.get('address')
        phone = data.get('phone')

        #입력필드 비었을때
        if not ID or not username or not dong_name or not password or not identification or not address or not phone:
            abort(400, description="Missing required fields")

        #입력정보가 이미 DB에 존재할 때
        existing_user = User.query.filter_by(id=ID).first()
        if existing_user:
            abort(400, description="User already exists")
        
        region = Region.query.filter_by(dong_name=dong_name).first()

        user = User(id=ID, identification = identification, username=username, address =address, phone = phone, region_id = region.id)
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
