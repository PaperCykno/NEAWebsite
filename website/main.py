from flask import Flask, render_template, request, redirect, url_for, flash
from __init__ import create_app, db
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Question, Choice, FormCreate


app = create_app()

@app.route('/', methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        
        form_Name = request.form.get('formName')
        form_Description = request.form.get('dsc')
        
        print(f"Form name: {form_Name}\nForm Description: {form_Description}")
        
        if FormCreate.query.filter_by(user_id=current_user.id, form_Name=form_Name).first():
            flash('Form Name already exist', category='error')
        else:
            forms = FormCreate(form_Name=form_Name, form_Description=form_Description, user_id=current_user.id)
            db.session.add(forms)
            db.session.commit()
            print(request.form)
            return redirect(url_for("form"))

    return render_template("home.html", user=current_user)


@app.route('/form', methods=["GET","POST"])
@login_required
def form():
    if request.method == "POST":
        question = request.form.get("question")
        choices = request.form.getlist("option")

        if question:
            form_create = FormCreate.query.filter_by(user_id=current_user.id).order_by(FormCreate.id.desc()).first()
            form_create_id = form_create.id

            poll = Question(question_text=question, user_id=current_user.id, FormCreate_id=form_create_id)

            db.session.add(poll)
            db.session.commit()
            print(request.form)

            for option in choices:
                newChoice = Choice(choice_text=option, question_id=poll.id)
                db.session.add(newChoice)
                db.session.commit()
                print(request.form)

        return redirect(url_for("polls"))
    return render_template("form.html", user=current_user)

@app.route('/polls')
@login_required
def polls():
    forms = FormCreate.query.filter_by(user_id=current_user.id).all()
    return render_template('polls.html', form_info = forms, user=current_user)
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    #print(request.form)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                #return redirect(url_for("home"))
                flash('Logged in successfully!', category='success')
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('Email Does not Exist', category='error')
    return render_template("log-in.html", user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.form)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        #if not email or not password:
        if User.query.filter_by(email=email).first():
            flash('Email already exists', category='error')
        else:
            user = User(
                email=email,
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha1')
                )
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            print(request.form)
            flash('Account Created!', category='success')
            #return redirect(url_for("login"))
    return render_template("register.html", user=current_user)   


#new routes for voting
@app.route('/polls/<int:question_id>', methods=['GET', 'POST'])
@login_required
def detail(question_id):
    question = Question.query.get(question_id)
    if request.method == 'POST':
        choice_id = request.form['choice']
        choice = Choice.query.get(choice_id)
        choice.votes += 1
        db.session.commit()
        return redirect(url_for('results', question_id=question.id))
    return render_template('detail.html', question=question, user=current_user)

@app.route('/polls/<int:question_id>/results')
@login_required
def results(question_id):
    question = Question.query.get(question_id)
    return render_template('results.html', question=question, user=current_user)


@app.route('/vote')
@login_required
def vote():
    return render_template('vote.html', user=current_user)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile_general.html', user=current_user)

@app.route('/profile_change_password', methods=['GET', 'POST'])
@login_required
def profile_change_password():
    if request.method == 'POST':
        old_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirmed_password')

        if check_password_hash(current_user.password, old_password):
            if new_password == confirm_password:
                current_user.password = generate_password_hash(new_password, method='pbkdf2:sha1')
                db.session.commit()
                flash('Password Changed', category='success')
            else:
                flash('Password does not match', category='error')
        else:
            flash('Old Password is incorrect', category='error')
    return render_template('profile_change_password.html', user=current_user)

@app.route('/profile_notifications', methods=['GET', 'POST'])
@login_required
def profile_notifications():
    if request.method == 'POST':
        notif_vote= request.form.get('vote_notification')
        if notif_vote == True:
            current_user.vote_notification = True
            db.session.commit()
            flash('Vote Notification Enabled', category='success')
        else:
            current_user.vote_notification = False
            db.session.commit()
            flash('Vote Notification Disabled', category='success')

    return render_template('profile_notifications.html', user=current_user)

@app.route('/allpollview')
@login_required
def allpollview():
    polls = FormCreate.query.filter_by().all()
    return render_template('allpollview.html', polls = polls, user=current_user)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
