from app import db
from datetime import datetime


class ProvinceInfo(db.Model):
    __tablename__ = 'province_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_time = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(255), nullable=False, unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)


class CityInfo(db.Model):
    __tablename__ = 'city_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_time = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(255), nullable=False, unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)