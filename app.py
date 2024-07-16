from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 로그인 페이지의 뷰 함수 이름
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://funcoding:funcoding@localhost/platform'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

# 데이터모델 클래스 -> DB에서 상호작용해야하는 테이블과 칼럼 써줘야할듯?
class data(db.Model):
    __tablename__ = '판매상품'  # 기존 테이블 이름이 '고객'임을 가정
    id = db.Column('ID', db.Integer, primary_key=True)
    residence_area = db.Column('거주지역')
    interest_item = db.Column('관심품목')

    def __repr__(self):
        return f'<Memo {self.title}>'


# 고객에 대한 클래스
class User(UserMixin, db.Model):
    __tablename__ = '고객' 
    id = db.Column('ID')
    username = db.Column('이름')
    residence_area = db.Column('거주지역')
    phone_num = db.Column('전화번호')
    password_hash = db.Column('비밀번호')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        ID = request.form['ID']
        username = request.form['username']
        phone_num = request.form['phone_num']
        residence_area = request.form['residence_area']
        password = request.form['password']
        
        user = User(id = ID, username=username, phone_num = phone_num,residence_area = residence_area)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Account created successfully'}), 201
    # GET 요청에 대해 JSON 형식의 응답 반환
    return jsonify({
        'message': 'Signup endpoint',
        'fields': {
            'ID': 'string',
            '거주지역' : 'string',
            'username': 'string',
            'phone_num': 'string',
            'password': 'string'
        }
    }), 200

def login():
    if request.method == 'POST':
        user = User.query.filter_by(ID=request.form['ID']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return jsonify({'message': 'Logged in successfully'}), 200
        return abort(401, description="Invalid credentials")
    abort(405) #로그인에서 GET은 X

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


####
@app.route("/")
def a():
    db = pymysql.connect(
    host='dd.ap-northeast-2.rds.amazonaws.com', 
    user='admin', 
    password='dd', 
    db='platform', 
    charset='utf8'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""SELECT * FROM platform.식재료 ORDER BY ID DESC LIMIT 1;""")
    result = cursor.fetchall()
    print(result)
    db.commit()
    db.close()
    return f"<p>{result}</p>"

if __name__ == "__main__":
    app.run(debug=True)