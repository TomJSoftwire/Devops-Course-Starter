# DevOps Apprenticeship: Project Exercise

For more details on the system's architecture see the diagrams in `todo-app-architecture.pdf`

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

## Environment Setup

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). Ensure the variables
in the env file are set as below

There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

| Variable     | Description                                                                                                                             |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| SECRET_KEY   | [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie. |
| TRELLO_KEY   | API key for the trello board used to track list status                                                                                  |
| TRELLO_TOKEN | API token used to manage the trello board                                                                                               |
| DONE_LIST_ID | The ID of the list containing completed task cards                                                                                      |

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:

```bash
$ poetry run flask run
```

You should see output similar to the following:

```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Running the app using ansible
To run the app using ansible copy the `/ansible/controller_files` folder to the controller node

Then update the inventory to include any additional host nodes and run the below command from inside the `controller_files` folder

`ansible-playbook playbook.yml -i inventory`

### Running the app using docker
To run the app using docker ensure docker daemon is running on your machine then

#### Development
Build the container by running `docker-compose -f docker-compose-dev.yml build`

Run the container using `docker-compose -f docker-compose-dev.yml -p 'todo-app-dev' up`

The dev site will then be available on `localhost:5000`

#### Production
Build the container by running `docker-compose -f docker-compose-prod.yml build`

Run the container using `docker-compose -f docker-compose-prod.yml -p 'todo-app-prod' up`

The production site will then be available on `0.0.0.0` (port 80)

## Running the tests

### Unit and Integration Tests

This project uses `pytest` for unit testing, run the tests with the command `poetry run pytest tests` or watch the tests using `poetry run ptw tests`.

To run individual tests append the test dir to the command used.

### E2E tests

To run the end to end tests run the command `poetry run pytest tests_e2e`
