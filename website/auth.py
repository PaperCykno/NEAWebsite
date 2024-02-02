from .__init__ import db
from flask import Blueprint, render_template, request, url_for, redirect
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
            return redirect('/home')
    return render_template("log-in.html", user=current_user)


@auth.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            return render_template("home.html", error="Please fill in all the fields")


        user = User(email=email, password=generate_password_hash(
            password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect('/home')
    return render_template("home.html")