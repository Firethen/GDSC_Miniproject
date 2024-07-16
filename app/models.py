from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify, abort
from flask import redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pymysql

db = SQLAlchemy()

#모델 전부다 클래스로 만들고, 필요한 함수가 더 있을란가 모르겠네.;

class order(db.Model):
    __tablename__ = '주문' 
    gid = db.Column('그룹ID')
    cid = db.Column('고객ID') 
    interest_item = db.Column('관심품목')


class User(db.Model):
    __tablename__ = '고객' 
    id = db.Column('ID')
    username = db.Column('이름')
    residence_area = db.Column('거주지역')
    phone_num = db.Column('전화번호')
    password_hash = db.Column('비밀번호')
    
class product(db.Model):
    __tablename__ = '공동구매그룹'
    gid = db.Column('공구그룹ID')
    market_id = db.Column('마켓ID')
    gradient_id = db.Column('상품ID')
