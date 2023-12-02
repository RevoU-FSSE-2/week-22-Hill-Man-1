# Import the required modules
import os
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman
from db import db
from task.apis import task_blueprint
from user.apis import user_blueprint
from common.bcrypt import bcrypt
from auth.apis import auth_blp

# Create the Flask app
app = Flask(__name__)

# Configure CORS with supports_credentials=True
CORS(app, origins=["http://localhost:3000"], supports_credentials=True, send_wildcard=True)

# Content security policy with Talisman
csp = {
    "default-src": "'self'",
}
Talisman(app, content_security_policy=csp)

# Configuration
database_url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

# Register blueprints
app.register_blueprint(auth_blp, url_prefix='/auth')
app.register_blueprint(task_blueprint, url_prefix='/task')
app.register_blueprint(user_blueprint, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
