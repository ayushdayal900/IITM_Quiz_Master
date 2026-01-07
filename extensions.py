from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "general_routes.login"

@login_manager.user_loader
def load_user(user_id):
    from models.models import User_Info
    return User_Info.query.get(int(user_id))
