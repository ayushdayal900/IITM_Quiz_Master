from datetime import datetime
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY'] = '124567890987654321!@#$%^&*())(*&^%$#@!)'

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
        if not admin_exists:
            admin = User_Info(id="0", email="admin@iitm.ac.in", password="123",  
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
