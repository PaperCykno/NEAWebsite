from flask import Flask, render_template, request, redirect, url_for
from website.views import views
from website import create_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User

db = SQLAlchemy()
DB_NAME = "database.db"

app = create_app()
app = Flask(__name__)
#app.register_blueprint(views, url_prefix='/')

@app.route('/')
def main_page():
    return render_template("website/template/home.html")
    #render_template(url_for('views.home'))


if __name__ == '__main__':
    app.run(debug=True)