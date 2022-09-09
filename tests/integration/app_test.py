import mongomock
import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app.app import create_app
from todo_app.data.item import ItemStatus
import pymongo


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = create_app()
        with test_app.test_client() as client:
            yield client


def test_index_page(client):
    mongo_client = pymongo.MongoClient('mongodb://fakemongo.com')
    db = mongo_client['db_name']
    collection = db['todo-items']
    collection.insert_one({
        'name': 'todo_card',
        'status': ItemStatus.TO_DO.value
    })
    response = client.get('/')

    assert response.status_code == 200
    assert 'todo_card' in response.data.decode()
