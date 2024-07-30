from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()

class Market(db.Model):
    __tablename__ = 'market'
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(50), nullable=False)  

class Region_Market(db.Model):
    __tablename__ = 'region_market_link'
    id = db.Column(db.Integer, primary_key=True)  # 
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)

class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)  # 
    dong = db.Column(db.String(30), nullable=False)  

class User(UserMixin, db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)  # 
    identification = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(5), nullable=False)  # 
    password = db.Column(db.String(20), nullable=False)  # 
    address = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)  # 
    name = db.Column(db.String(50))

class Gonggu_product(db.Model):
    __tablename__ = 'gonggu_product'
    id = db.Column(db.Integer, primary_key=True)  # 
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)


class Product_like(db.Model):
    __tablename__ = 'product_like'
    id = db.Column(db.Integer, primary_key=True)  # 
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    gonggu_product_id = db.Column(db.Integer, db.ForeignKey('gonggu_product.id'), nullable=False)

class Market_like(db.Model):
    __tablename__ = 'market_like'
    id = db.Column(db.Integer, primary_key=True)  # 
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)

class Keyword(db.Model):
    __tablename__ = 'keyword'
    id = db.Column(db.Integer, primary_key=True)  # 
    keyword = db.Column(db.String(30), nullable=False)  # 

class Keyword_market_link(db.Model):
    __tablename__ = 'keyword_market_link'
    id = db.Column(db.Integer, primary_key=True)  # 
    keyword_id = db.Column(db.Integer, db.ForeignKey('keyword.id'), nullable=False)
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'), nullable=False)

class Purchase(db.Model):
    __tablename__ = 'purchase'
    id = db.Column(db.Integer, primary_key=True)  # 
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    gonggu_group_id = db.Column(db.Integer, db.ForeignKey('gonggu_group.id'), nullable=False)

class Gonggu_group(db.Model):
    __tablename__ = 'gonggu_group' 
    id = db.Column(db.Integer, primary_key=True)  # 
    gonggu_product_id = db.Column(db.Integer, db.ForeignKey('gonggu_product.id'), nullable=False)
    size = db.Column(db.Integer, nullable=False)