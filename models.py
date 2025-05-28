from extensions import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    plans = db.relationship('StudyPlan', backref='user', lazy=True)


class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    plan = db.Column(db.Text, nullable=False)
    planned_date = db.Column(db.Date, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

