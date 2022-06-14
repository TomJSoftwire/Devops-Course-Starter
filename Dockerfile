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
COPY start.py .
COPY wsgi.py .
COPY prod-start.sh .
RUN chmod +x ./prod-start.sh

ENTRYPOINT ./prod-start.sh

FROM base as dev_base
RUN poetry install

FROM dev_base as development
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM dev_base as test
 
# Install the long-term support version of Firefox (and curl if you don't have it already)
RUN apt-get install -y firefox-esr curl
  
# Download geckodriver and put it in the usr/bin folder
ENV GECKODRIVER_VER v0.30.0
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz

COPY todo_app todo_app
COPY tests tests
COPY tests_e2e tests_e2e

ENTRYPOINT ["poetry", "run", "pytest"]