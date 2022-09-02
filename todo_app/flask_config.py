import os


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
        
        if not self.SECRET_KEY:
            raise ValueError(
                "No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
