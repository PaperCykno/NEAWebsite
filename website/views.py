from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, login_user

views = Blueprint('views', __name__)

@views.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html")

#@views.route('/login', methods=['GET', 'POST'])
#def login():
    #return render_template("log-in.html")

