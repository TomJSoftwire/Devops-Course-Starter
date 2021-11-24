from flask import Flask, render_template, redirect
from flask.globals import request
from todo_app.data.trello_items import get_item, add_item, get_items, save_item
import sys

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=get_items())


@app.route('/item', methods=['POST', 'PUT'])
def item():
    if(request.method == 'POST'):
        args = request.args
        if(len(args) > 0):
            id = args.get('id')
            item = get_item(id)
            status = args.get('status')
            updated_item = {'id': id, 'status': status, 'title': item.title}
            save_item(updated_item)
        else:
            form = request.form
            title = form.get('title')
            add_item(title)
    return redirect('/')
