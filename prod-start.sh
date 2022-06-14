#!/bin/sh
poetry run gunicorn wsgi:start -b 0.0.0.0:$PORT