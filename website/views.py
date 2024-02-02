from flask import Blueprint, render_template, request, url_for, redirect

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def signup():
    return render_template("register.html")

@views.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@views.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("log-in.html")