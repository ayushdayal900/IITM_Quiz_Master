from datetime import datetime
from flask import Flask
from controllers.routes import gen, dB, admin, user  # Import controllers
from models.models import User_Info, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'


db.init_app(app)  # Initialize database

# Register Blueprints
app.register_blueprint(gen)
app.register_blueprint(dB)
app.register_blueprint(admin)
app.register_blueprint(user)


def initialize_database():
    with app.app_context():
        db.create_all() 
        
        admin_exists = User_Info.query.filter_by(id="0").first()
        if not admin_exists:
            admin = User_Info(id="0",email="admin@iitm.ac.in",password="123",  full_name="Admin Admin",qualification="12th",role=0, dob=datetime.strptime("2025-03-12", "%Y-%m-%d").date())
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")

    
if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)

