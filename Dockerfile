FROM python:3.11-rc
RUN apt-get update 
RUN pip3 install 'poetry==1.1.11'

WORKDIR /todo-app

COPY poetry.lock .
COPY poetry.toml .
COPY pyproject.toml .
COPY todo_app todo_app
RUN poetry install --no-dev

WORKDIR /todo-app/todo_app

ENTRYPOINT poetry run gunicorn wsgi:start -b 0.0.0.0:80