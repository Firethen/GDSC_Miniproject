from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify, abort
from flask import redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pymysql

db = SQLAlchemy()

#모델 전부다 클래스로 만들고, 필요한 함수가 더 있을란가 모르겠네.;

class Market(db.Model):
    __tablename__ = 'market' 
    market_id = db.Column('id')
    market_name = db.Column('name')

class Region_Market(db.Model):
    __tablename__ = 'region_market_link'
    region_market_id = db.Column('id')
    region_id = db.Column('region_id')
    market_id = db.Column('market_id') 

class Region(db.Model):
    __tablename__ = 'region'
    r_id = db.Column('id')
    dong_name = db.Column('dong')   #동 이름

class User(UserMixin, db.Model):
    __tablename__ = 'customer' 
    id = db.Column('id')
    identification = db.Column('identification')
    username = db.Column('name')
    password_hash = db.Column('password')
    address = db.Column('address')
    phone = db.Column('phone')
    region_id = db.Column('region_id')
    #zzim = db.Column('관심상품')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column('id')
    name = db.Column('name')

class Gonggu_product(db.Model):
    __tablename__ = 'gonggu_product'
    id = db.Column('id')
    market_id = db.Column('market_id')
    product_id = db.Column('product_id')
    price = db.Column('price')

class Product_like(db.Model):
    __tablename__ = 'product_like'
    id = db.Column('id')
    customer_id = db.Column('customer_id')
    product_id = db.Column('product_id')

class Market_like(db.Model):
    __tablename__ = 'market_like'
    id = db.Column('id')
    customer_id = db.Column('customer_id')
    market_id = db.Column('market_id')

class Keyword(db.Model):
    __tablename__ = 'keyword'
    id = db.Column('id')
    keyword_name = db.Column('keyword')

class Keyword_market_link(db.Model):
    __tablename__ = 'keyword_market_link'
    id = db.Column('id')
    keyword_id = db.Column('keyword_id')
    market_id = db.Column('market_id')

class Purchase(db.Model):
    __tablename__ = 'purchase'
    id = db.Column('id')
    customer_id = db.Column('customer_id')
    group_id = db.Column('gonggu_group_id')

class Gonggu_product(db.Model):
    __tablename__ = 'gonggu_product'
    id = db.Column('id')
    product_id = db.Column('gonggu_product_id')
    size = db.Column('size')

#---------------------------------------
class Order(db.Model):
    __tablename__ = '주문' 
    gid = db.Column('그룹ID')
    user_id = db.Column('고객ID') 
    interest_item = db.Column('관심품목')
    quantity = db.Column('수량')


class Group(db.Model):
    __tablename__ = '그룹'
    gid = db.Column('그룹ID')
    product_id = db.Column('상품ID')
    market_id = db.Column('마켓ID')
    max_size = db.Column('최대규모')
    current_size = db.Column('현재규모')
