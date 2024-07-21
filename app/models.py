from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()

class Market(db.Model):
    __tablename__ = 'market'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    name = db.Column(db.String(50), nullable=False)  # 컬럼명 수정

class Region_Market(db.Model):
    __tablename__ = 'region_market_link'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)

class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    dong = db.Column(db.String(30), nullable=False)  # 컬럼명 수정

class User(UserMixin, db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    identification = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(5), nullable=False)  # 컬럼명 수정
    password_hash = db.Column(db.String(20), nullable=False)  # 컬럼명 수정
    address = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    name = db.Column(db.String(50))

class Gonggu_product(db.Model):
    __tablename__ = 'gonggu_product'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Product_like(db.Model):
    __tablename__ = 'product_like'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

class Market_like(db.Model):
    __tablename__ = 'market_like'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)

class Keyword(db.Model):
    __tablename__ = 'keyword'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    keyword = db.Column(db.String(30), nullable=False)  # 컬럼명 수정

class Keyword_market_link(db.Model):
    __tablename__ = 'keyword_market_link'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    keyword_id = db.Column(db.Integer, db.ForeignKey('keyword.id'), nullable=False)
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)

class Purchase(db.Model):
    __tablename__ = 'purchase'
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    gonggu_group_id = db.Column(db.Integer, db.ForeignKey('gonggu_group.id'), nullable=False)

class Gonggu_group(db.Model):
    __tablename__ = 'gonggu_group'  # 테이블명 수정
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    gonggu_product_id = db.Column(db.Integer, db.ForeignKey('gonggu_product.id'), nullable=False)
    size = db.Column(db.Integer, nullable=False)

# ---------------------------------------
class Order(db.Model):
    __tablename__ = 'order'  # 테이블명 수정
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    gid = db.Column(db.Integer, nullable=False)  # 그룹ID
    user_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)  # 고객ID
    interest_item = db.Column(db.String(255))  # 관심품목
    quantity = db.Column(db.Integer)  # 수량

class Group(db.Model):
    __tablename__ = 'group'  # 테이블명 수정
    id = db.Column(db.Integer, primary_key=True)  # 컬럼명 수정 및 primary key 설정
    gid = db.Column(db.Integer, nullable=False)  # 그룹ID
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # 상품ID
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)  # 마켓ID
    max_size = db.Column(db.Integer, nullable=False)  # 최대규모
    current_size = db.Column(db.Integer, nullable=False)  # 현재규모
