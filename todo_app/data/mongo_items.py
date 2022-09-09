from flask import session
import pymongo
from bson import ObjectId
from todo_app.flask_config import Config
from todo_app.data.item import Item, ItemStatus

def get_items_collection():
    client = pymongo.MongoClient(Config().mongo_connection_string)
    db = client[Config().mongo_db_name]
    return db['todo-items']

def get_items():
    items = get_items_collection()

    allItems = items.find()
    return [Item.from_mongo_document(item) for item in allItems]

def get_item(id):
    items = get_items_collection()

    item_by_id = items.find_one({'_id': ObjectId(id)})

    return Item.from_mongo_document(item_by_id)


def add_item(title):
    items = get_items_collection()
    items.insert_one({
        'name': title,
        'status': ItemStatus.TO_DO.value
    })

    return Item('test', 'Test')


def save_item(item):
    items = get_items_collection()

    items.update_one({'_id': ObjectId(item['id'])}, {"$set": {'status': item['status']}})


# def create_todo_board():
#     try:
#         r = trello_post(f'boards', {'name': 'app_e2e_test_board', 'idOrganization': Config().organisation_id })
#         response = r.json()
#         return response['id']
#     except Exception as e:
#         print('failed to create board')
#         raise Exception(e)

# def delete_todo_board(boardId):
#     r = trello_delete(f'boards/{boardId}', {})