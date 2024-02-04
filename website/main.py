from flask import Flask, render_template, request, redirect, url_for, flash
from views import views
from __init__ import create_app, db
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User


db = SQLAlchemy()
DB_NAME = "database.db"

app = create_app()
app = Flask(__name__)

#app.register_blueprint(views, url_prefix='/')

@app.route('/')
def main_page():
    return render_template("home.html")
    #render_template(url_for('views.home'))

@app.route('/vote')
def vote():
    return render_template("vote.html")

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/poll')
def poll():
    return render_template("poll.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash("Incorrect Password")
        else:
            flash("Email Doesn't Exist")
    return render_template("log-in.html", user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash('Email already exist')
        else:
            user = User(email=email, password=generate_password_hash(
            password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for("home"))
    return render_template("register.html")   




if __name__ == '__main__':
    app.run(debug=True)