import os
import logging

class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.env = os.getenv('FLASK_ENV')
        self.mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')
        self.mongo_db_name = os.getenv('MONGO_DB_NAME')
        self.github_app_id = os.getenv('OAUTH_APP_ID')
        self.github_app_secret = os.getenv('OAUTH_APP_SECRET')
        self.LOGIN_DISABLED = os.getenv('LOGIN_DISABLED')
        self.LOG_LEVEL = os.getenv('LOG_LEVEL')
        self.LOGGLY_TOKEN = os.getenv('LOGGLY_TOKEN')
        if not self.SECRET_KEY:
            raise ValueError(
                "No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
