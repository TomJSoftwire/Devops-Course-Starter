import os
import logging

class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.api_key = os.getenv('TRELLO_KEY')
        self.api_token = os.getenv('TRELLO_TOKEN')
        self.organisation_id = os.getenv('BOARD_ORGANISATION_ID')
        self.board_id = os.getenv('BOARD_ID')
        self.mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')
        self.mongo_db_name = os.getenv('MONGO_DB_NAME')
        self.github_app_id = os.getenv('GITHUB_APP_ID')
        self.github_app_secret = os.getenv('GITHUB_APP_SECRET')

        self.LOGIN_DISABLED = os.getenv('LOGIN_DISABLED') == 'True'
        
        if not self.SECRET_KEY:
            raise ValueError(
                "No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
