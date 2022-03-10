FROM python:3.11-rc
RUN apt-get update 
RUN pip3 install --upgrade --force pip
RUN pip3 install poetry

WORKDIR /todo-app
COPY .env .
COPY poetry.lock .
COPY poetry.toml .
COPY pyproject.toml .
COPY todo_app todo_app
RUN poetry install --no-dev

COPY prod_start.sh .

ENTRYPOINT sh prod_start.sh