'''from flask import Flask, render_template, request, jsonify, abort
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 로그인 페이지의 뷰 함수 이름

db = SQLAlchemy(app)




#
@app.route('/user/create', methods=['POST'])
def create_memo():
    title = request.json['title']
    content = request.json['content']
    new_memo = Memo(title=title, content=content)
    db.session.add(new_memo)
    db.session.commit()
    return jsonify({'message': 'Memo created'}), 201

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
    app.run(debug=True)'''