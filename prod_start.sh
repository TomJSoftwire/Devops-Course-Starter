#!/bin/bash

export $(grep -v '^#' .env )
cd ./todo_app
poetry run gunicorn wsgi:start -b 0.0.0.0:80
