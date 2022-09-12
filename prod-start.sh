#!/bin/sh
echo $FLASK_APP
echo $FLASK_ENV
echo $SECRET_KEY
echo $PORT
echo $MONGO_CONNECTION_STRING
echo $MONGO_DB_NAME
echo $OAUTH_APP_ID
echo $OAUTH_APP_SECRET
poetry run gunicorn 'todo_app.app:create_app()' -b 0.0.0.0:$PORT
