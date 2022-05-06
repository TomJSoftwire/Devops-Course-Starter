FROM python:3.11.0a6-slim-buster as base

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev

RUN pip3 install 'poetry==1.1.11' \
    && poetry config virtualenvs.create false

WORKDIR /todo-app
COPY poetry.lock poetry.toml pyproject.toml ./

FROM base as production
RUN poetry install --no-dev
COPY todo_app todo_app
WORKDIR /todo-app/todo_app

ENTRYPOINT poetry run gunicorn wsgi:start -b 0.0.0.0:80

FROM base as dev_base
RUN poetry install

FROM dev_base as development
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM dev_base as test
COPY todo_app todo_app
COPY tests tests
WORKDIR /todo-app
ENTRYPOINT poetry run pytest
