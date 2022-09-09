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
COPY prod-start.sh .
RUN chmod +x ./prod-start.sh

ENTRYPOINT ./prod-start.sh

FROM base as development
RUN poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base as test
 
# Install the long-term support version of Firefox (and curl if you don't have it already)
RUN apt-get install -y firefox-esr curl
  
# Download geckodriver and put it in the usr/bin folder
ENV GECKODRIVER_VER v0.30.0
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz

RUN poetry install

COPY todo_app todo_app
COPY tests tests
COPY tests_e2e tests_e2e

ENTRYPOINT ["poetry", "run", "pytest"]