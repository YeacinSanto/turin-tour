import os
from flask import Flask 
from flask_login import LoginManager
from dotenv import load_dotenv

from dao.user_dao import get_user_by_id
from routes.auth_route import auth_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    
    app.config['UPLOAD_FOLDER_PROMO'] = os.path.join(app.static_folder,'uploads','tours')
    
    app.config['UPLOAD_FOLDER_REPORTS'] = os.path.join(app.static_folder,'uploads', 'reports')
    
    os.makedirs(app.config['UPLOAD_FOLDER_PROMO'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_REPORTS'], exist_ok=True)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)
    
    app.register_blueprint(auth_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
