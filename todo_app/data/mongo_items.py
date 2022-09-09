import pymongo
from bson import ObjectId
from todo_app.flask_config import Config
from todo_app.data.item import Item, ItemStatus

db_client = None

def load_db_client():
    global db_client
    if db_client is None:
        db_client = pymongo.MongoClient(Config().mongo_connection_string)
    return db_client

def get_items_collection():
    client = load_db_client()
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

def save_item(item):
    items = get_items_collection()

    items.update_one({'_id': ObjectId(item['id'])}, {"$set": {'status': item['status']}})

def delete_todo_board():
    client = load_db_client()
    client.drop_database(Config().mongo_db_name)