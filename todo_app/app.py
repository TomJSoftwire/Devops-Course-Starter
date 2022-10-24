from flask import Flask, render_template, redirect
from flask.globals import request
from todo_app.data.mongo_items import get_item, get_items, add_item, save_item
from flask_login import login_required, current_user
from todo_app.view_model import ViewModel
from todo_app.flask_config import Config
from flask import redirect
from flask_login import LoginManager, login_user 
from requests import post, get
import json
from todo_app.user import writers_only, User
from logging import error


def create_app():

    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)

    login_manager = LoginManager()
    if config.env == 'test':
        login_manager.anonymous_user = lambda : User('74607461')

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(f'https://github.com/login/oauth/authorize?client_id={config.github_app_id}')

    @login_manager.user_loader
    def load_user(user_id):
        if user_id is None or user_id == 'None':
            return None
        return User(user_id)

    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        view_model = ViewModel(get_items(), current_user.role)
        return render_template('index.html', view_model=view_model)


    @app.route('/item', methods=['POST', 'PUT'])
    @login_required
    @writers_only
    def item():
        if(request.method == 'POST'):
            args = request.args
            if(len(args) > 0):
                id = args.get('id')
                item = get_item(id)
                status = args.get('status')
                updated_item = {
                    'id': id, 'status': status, 'title': item.title}
                save_item(updated_item)
            else:
                form = request.form
                title = form.get('title')
                add_item(title)
        return redirect('/')

    @app.route('/login/callback')
    def login():
        github_code = request.args.get('code')
        params = {'client_id': config.github_app_id,
                  'client_secret': config.github_app_secret,
                  'code': github_code
                  }
        token_request = post('https://github.com/login/oauth/access_token',
                             params=params, headers={'Accept': 'application/json'})
        token = json.loads(token_request.text).get('access_token')
        user_info_request = get('https://api.github.com/user', headers={
                                'Authorization': f'Bearer {token}', 'Accept': 'application/json'})
        user_info = json.loads(user_info_request.text)
        user_id = user_info.get("id")
        if user_id is None:
            error('app did not authorise correctly')
            return redirect('/error')
        user = User(user_id)
        login_user(user)
        return redirect('/')

    return app
