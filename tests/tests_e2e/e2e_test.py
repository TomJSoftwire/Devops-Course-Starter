import os
import time
import threading
from dotenv.main import find_dotenv, load_dotenv
import pytest
from todo_app.app import create_app
from todo_app.data.trello_items import create_todo_board, delete_todo_board
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def app_with_test_board():

    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    board_id = create_todo_board()

    os.environ['BOARD_ID'] = board_id

    app = create_app()

    thread = threading.Thread(target=lambda: app.run(use_reloader=False)) 
    thread.daemon = True 
    thread.start() 
    # This was necessary to allow the app time to load before the test begins
    time.sleep(1)
    yield app 

    # Tear Down 
    thread.join(1) 
    print('del board')
    delete_todo_board(board_id)

@pytest.fixture(scope='module')
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(app_with_test_board, driver):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
  
