from flask import Flask, render_template, redirect
from flask.globals import request
from todo_app.data.trello_items import get_item, get_items, save_item
from todo_app.data.mongo_items import add_item

from todo_app.view_model import ViewModel
from todo_app import flask_config

def create_app():

    app = Flask(__name__)
    app.config.from_object(flask_config.Config())

    @app.route('/')
    def index():
        view_model = ViewModel(get_items())
        return render_template('index.html', view_model=view_model)

    @app.route('/item', methods=['POST', 'PUT'])
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