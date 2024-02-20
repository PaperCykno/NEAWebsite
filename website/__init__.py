from os import path
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kapuishon'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from models import User, Question, FormCreate, Choice
    '''
    with app.app_context():
        #db.create_all()
        try :
            db.create_all()
        except Exception as e:
            print(f"Got the following exception {e} while creating the database.")
        finally:
            print("db.create_all() in __init__.py was successful. No exception was raised")
            from models import User
    '''
    
    # Create an application context to work within the Flask application
    with app.app_context():
        try:
            # Attempt to create all database tables
            db.create_all()
        except Exception as e:
            # Handle any exceptions that occur during database creation
            print(f"Got the following exception {e} while creating the database.")
        finally:
            # Print a success message after attempting to create all tables
            print("db.create_all() in __init__.py was successful. No exception was raised")
            # Import the User model after creating the database tables
            from models import User



    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

    return app

def create_database(app):
    if path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')


