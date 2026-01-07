from datetime import datetime
from flask import Flask
from controllers.Resource_api import *
from extensions import db, login_manager, bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = "1234567890!@#$%^&*()"

# Initialize Extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

def init_blueprints():
    # avoid circular import
    from controllers.routes import gen, data, admin, user  

    app.register_blueprint(gen)
    app.register_blueprint(data)
    app.register_blueprint(admin)
    app.register_blueprint(user)

from models.models import User_Info

# Initialize application components
with app.app_context():
    db.create_all()
    # Check/Create Admin
    admin_exists = User_Info.query.filter_by(id="0").first()
    if not admin_exists:
        hashed_password = bcrypt.generate_password_hash("123").decode('utf-8')
        admin = User_Info(id="0", email="admin@iitm.ac.in", 
                          password=hashed_password,  
                          full_name="Admin Admin", qualification="12", 
                          role=0, dob=datetime.strptime("2025-03-12", "%Y-%m-%d").date())
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")

# Register Blueprints & API
init_blueprints()
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
