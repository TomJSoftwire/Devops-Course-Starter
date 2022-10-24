from flask_login import UserMixin, current_user
from flask import abort
from todo_app.flask_config import Config

class User(UserMixin):
    def __init__(self, id) -> None:
        super().__init__()
        self.id = id
        self.role = 'writer' if id == '74607461' else 'reader'

def writers_only(func):
    def wrapper():
        if Config().LOGIN_DISABLED or current_user.role == 'writer':
            return func()
        else:
            abort(401)
    return wrapper
