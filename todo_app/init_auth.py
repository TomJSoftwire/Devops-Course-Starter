from flask import redirect
from flask_login import LoginManager
from todo_app.flask_config import Config

def init_auth(app):
    login_manager = LoginManager()
    config = Config()

    @login_manager.unauthorized_handler
    def unauthenticated():
        redirect(f'https://github.com/login/oauth/authorize?client_id={config.github_app_id}')

    @login_manager.user_loader
    def load_user(user_id):
        pass

    login_manager.init_app(app)