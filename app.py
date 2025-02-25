from flask import Flask
from controllers.routes import gen, dB, admin, user  # Import controllers
from models.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'


db.init_app(app)  # Initialize database

# Register Blueprints
app.register_blueprint(gen)
app.register_blueprint(dB)
app.register_blueprint(admin)
app.register_blueprint(user)

    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

