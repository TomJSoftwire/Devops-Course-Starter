from flask import Flask, render_template, redirect
from flask.globals import request
from todo_app.data.mongo_items import get_item, get_items, add_item, save_item
from flask_login import login_required
from todo_app.view_model import ViewModel
from todo_app import flask_config
from flask import redirect
from flask_login import LoginManager
from todo_app.flask_config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(flask_config.Config())

    login_manager = LoginManager()
    config = Config()

    @login_manager.unauthorized_handler
    def unauthenticated():
        print('redirecting')
        return redirect(f'https://github.com/login/oauth/authorize?client_id={config.github_app_id}')

    @login_manager.user_loader
    def load_user(user_id):
        pass

    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        view_model = ViewModel(get_items())
        return render_template('index.html', view_model=view_model)

    @app.route('/item', methods=['POST', 'PUT'])
    @login_required
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

    return app
