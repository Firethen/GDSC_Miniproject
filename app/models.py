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


class User(UserMixin, db.Model):
    __tablename__ = '고객' 
    id = db.Column('고객ID')
    username = db.Column('이름')
    residence_area = db.Column('지역')
    password_hash = db.Column('password')
    zzim = db.Column('관심상품')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
class product(db.Model):
    __tablename__ = '상품'
    pid = db.Column('상품ID')
    market_id = db.Column('마켓ID')
    category = db.Column('카테고리')
    name = db.Column('상품명')
