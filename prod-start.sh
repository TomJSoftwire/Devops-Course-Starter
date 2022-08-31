#!/bin/sh
poetry run gunicorn 'todo_app.app:create_app()' -b 0.0.0.0:$PORT