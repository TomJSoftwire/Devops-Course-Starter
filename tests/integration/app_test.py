import os
import requests
import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app.app import create_app


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = create_app()

    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', get_lists_stub)
    response = client.get('/')

    assert response.status_code == 200
    assert 'todo_card' in response.data.decode()

class StubResponse():
    def __init__(self, fake_response_data) -> None:
        self.fake_response_data = fake_response_data
        self.status_code = 200

    def json(self):
        return self.fake_response_data

def get_lists_stub(url, params):
    test_todo_list_id = 'test_todo_list_id'
    test_done_list_id = 'test_done_list_id'
    test_board_id = os.environ.get('BOARD_ID')

    fake_response_data = None

    if url == f'https://api.trello.com/1/list/{test_todo_list_id}/cards/':
        fake_response_data = [{'id': '1', 'name': 'todo_card', 'idList': test_todo_list_id}]
    if url == f'https://api.trello.com/1/list/{test_done_list_id}/cards/':
        fake_response_data = [{'id': '2', 'name': 'done_card', 'idList': test_done_list_id}]
    if url == f'https://api.trello.com/1/board/{test_board_id}/lists/':
        fake_response_data = [{'id': test_done_list_id, 'name': 'To Do'},{'id': test_todo_list_id, 'name': 'Done'}]

    
    return StubResponse(fake_response_data)
