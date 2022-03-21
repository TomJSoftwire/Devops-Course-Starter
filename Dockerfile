FROM python:3.11-rc as base
RUN apt-get update 
RUN pip3 install 'poetry==1.1.11'

WORKDIR /todo-app
COPY poetry.lock .
COPY poetry.toml .
COPY pyproject.toml .
COPY todo_app todo_app

FROM base as production
RUN poetry install --no-dev
WORKDIR /todo-app/todo_app

ENTRYPOINT poetry run gunicorn wsgi:start -b 0.0.0.0:80

FROM base as development
RUN poetry install

ENTRYPOINT poetry run flask run --host=0.0.0.0