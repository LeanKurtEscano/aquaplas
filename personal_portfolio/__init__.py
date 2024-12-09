from flask import Flask
from personal_portfolio.auth.auth import auth
from .all_blueprint.blueprint import blueprint
from .all_blueprint.profile import pr
from .all_blueprint.crud import cr
from .all_blueprint.blog import bl

def create_app():
    app = Flask(__name__)
    
    app.secret_key = 'sdkjfhvsjkdhfvkshjdvf'
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(blueprint,url_prefix='/dashboard')
    app.register_blueprint(pr,url_prefix = '/profile')
    app.register_blueprint(cr,url_prefix = '/crud')
    app.register_blueprint(bl,url_prefix = '/blog')
    
    return app