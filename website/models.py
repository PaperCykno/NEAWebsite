from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    notifications = db.Column(db.Boolean, default=False)
    question = db.relationship('Question')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    FormCreate_id = db.Column(db.Integer, db.ForeignKey('form_create.id'), nullable=False)



class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    choice_text = db.Column(db.String(200), nullable=False)
    votes = db.Column(db.Integer, default=0)

    question = db.relationship('Question', backref=db.backref('choices', lazy=True))

class FormCreate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_Name = db.Column(db.String(200), nullable=False)
    form_Description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    user = db.relationship('User', backref=db.backref('form_creates', lazy=True))
