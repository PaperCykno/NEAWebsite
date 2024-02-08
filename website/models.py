from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    question = db.relationship('Question')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    #pub_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    FormCreate_id = db.Column(db.Integer, db.ForeignKey('form_create.id'), nullable=False)

    def __repr__(self):
        return '<Question %r>' % self.question_text


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    choice_text = db.Column(db.String(200), nullable=False)
    votes = db.Column(db.Integer, default=0)

    question = db.relationship('Question', backref=db.backref('choices', lazy=True))

    def __repr__(self):
        return '<Choice %r>' % self.choice_text

class FormCreate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_Name = db.Column(db.String(200), nullable=False)
    form_Description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #date_created = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<FormCreate %r>' % self.form_name

'''
class Question( models.Model):
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')

  def __str__(self):
    return self.question_text

class Choice( models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

  def __str__(self):
    return self.choice_text

class FormCreate(models.Model):
  form_name = models.CharField(max_length=200)
  form_description = models.CharField(max_length=200)
  date_created = models.DateTimeField('date created')
'''