#!/bin/sh
poetry run gunicorn todo_app.wsgi:start -b 0.0.0.0:$PORT