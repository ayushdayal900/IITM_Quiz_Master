from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY'] = bcrypt.generate_password_hash("supersecretkey").decode('utf-8')

login_manager = LoginManager(app)
login_manager.login_view = "general_routes.login"


@login_manager.user_loader
def load_user(user_id):
    return User_Info.query.get(int(user_id))



def init_blueprints():
    # Import inside function to avoid circular import
    from controllers.routes import gen, data, admin, user  

    app.register_blueprint(gen)
    app.register_blueprint(data)
    app.register_blueprint(admin)
    app.register_blueprint(user)

from models.models import User_Info, db
def initialize_database():
    with app.app_context():
        db.create_all() 
        
        admin_exists = User_Info.query.filter_by(id="0").first()
        hashed_password = bcrypt.generate_password_hash("123").decode('utf-8')
        if not admin_exists:
            admin = User_Info(id="0", email="admin@iitm.ac.in", 
                              password=hashed_password,  
                              full_name="Admin Admin", qualification="12", 
                              role=0, dob=datetime.strptime("2025-03-12", "%Y-%m-%d").date())
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")


db.init_app(app)  # Initialize database
if __name__ == '__main__':
    initialize_database()
    init_blueprints()  
    app.run(debug=True)
