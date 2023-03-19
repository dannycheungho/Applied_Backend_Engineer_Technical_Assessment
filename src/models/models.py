from flask_sqlalchemy import SQLAlchemy
from src.meta.category_enum import CategoryEnum
from src.meta.district_enum import DistrictEnum

db = SQLAlchemy()

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    districts = db.relationship('District', backref='doctor', lazy=True)
    categories = db.relationship('Category', backref='doctor', lazy=True)
    doctorTranslation = db.relationship('DoctorTranslation', backref='doctor', lazy=True)

class DoctorTranslation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    language_id = db.Column(db.Integer)
    name = db.Column(db.String(50), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    district_name = db.Column(db.Enum(DistrictEnum), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    clinic_phone = db.Column(db.Integer, nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    price_remark = db.Column(db.String(20))
    working_time = db.Column(db.String(50), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    districtTranslation = db.relationship('DistrictTranslation', backref='district', lazy=True)

    def __repr__(self):
        return f'<District {self.district_name,self.address,self.price_remark,}>'

class DistrictTranslation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    language_id = db.Column(db.Integer)
    district_name = db.Column(db.Enum(DistrictEnum), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    price_remark = db.Column(db.String(20))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)  

    def __repr__(self):
        return f'<DistrictTranslation {self.district_name,self.address,self.price_remark,}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.Enum(CategoryEnum), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    categoryTranslation = db.relationship('CategoryTranslation', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.category_name}>'

class CategoryTranslation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    language_id = db.Column(db.Integer)
    category_name = db.Column(db.Enum(CategoryEnum), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
