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
        logging.error(self.SECRET_KEY)
        logging.error(self.api_key)
        logging.error(self.api_token)
        logging.error(self.organisation_id)
        logging.error(self.board_id)
        logging.error(self.mongo_connection_string)
        logging.error(self.mongo_db_name)
        if not self.SECRET_KEY:
            raise ValueError(
                "No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
