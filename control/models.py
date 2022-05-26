from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(150))
    job_description = db.Column(db.String(150))
    image = db.Column(db.String(500), nullable=True, default="")
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    gender = db.Column(db.String(10))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))


class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(500), nullable=True, default="")
    description = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    employees = db.relationship("Employee")
