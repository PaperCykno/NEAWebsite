from flask import Flask, render_template, request, redirect, url_for, flash
from views import views
from __init__ import create_app, db
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Question, Choice, FormCreate


#db = SQLAlchemy()
#DB_NAME = "database.db"

app = create_app()
#app = Flask(__name__)


@app.route('/', methods=["GET","POST"])
def home():
    if request.method == "POST":
        form_Name = request.form.get('formName')
        form_Description = request.form.get('dsc')
        form = FormCreate(formName=form_Name, dsc=form_Description)
        db.session.add(form)
        db.session.commit()
        print(request.form)
        return redirect(url_for("form"))
    return render_template("home.html")

@app.route('/vote')
def vote():
    return render_template("vote.html")

@app.route('/form', methods=["GET","POST"])
def form():
    if request.method == "POST":
        question = request.form.get("question")
        choices = request.form.getlist("option")

        poll = Question(question=question)

        db.session.add(poll)
        db.session.commit()

        for option in choices:
            newOption = Choice(choice_text=option, question_id=poll.id)
            db.session.add(newOption)
            db.session.commit()
        return render_template("home.html")
    return render_template("form.html")

@app.route('/poll')
def poll():
    return render_template("poll.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("log-in.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.form)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash("Incorrect Password", )
        else:
            flash("Email Doesn't Exist")
    return render_template("log-in.html", user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.form)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #if not email or not password:
        if User.query.filter_by(email=email).first():
            flash('Email already exist', category="error")
        else:
            user = User(
                email=email,
                password=generate_password_hash(password, method='pbkdf2:sha1')
                )
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            print(request.form)
            return redirect(url_for("login"))
    return render_template("register.html")   



if __name__ == '__main__':
    app.run(debug=True, port=5001)