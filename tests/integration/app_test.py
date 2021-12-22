import os
import requests
import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app.app_builder import create_app


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    print(file_path)
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
    test_todo_list_id = os.environ.get('TODO_LIST_ID')
    test_done_list_id = os.environ.get('DONE_LIST_ID')

    fake_response_data = None

    if url == f'https://api.trello.com/1/list/{test_todo_list_id}/cards/':
        fake_response_data = [{'id': '1', 'name': 'todo_card', 'idList': test_todo_list_id}]
    if url == f'https://api.trello.com/1/list/{test_done_list_id}/cards/':
        fake_response_data = [{'id': '2', 'name': 'done_card', 'idList': test_done_list_id}]
    
    return StubResponse(fake_response_data)
