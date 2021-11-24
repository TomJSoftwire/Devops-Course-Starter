from flask import Flask, render_template, redirect
from flask.globals import request
from todo_app.data.session_items import add_item, get_items

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items = get_items())

@app.route('/item', methods = ['POST'])
def item():
    form = request.form
    title = form.get('title')
    add_item(title)
    return redirect('/')
