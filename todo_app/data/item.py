import os
from enum import Enum

class ItemStatus(Enum):
    TO_DO = 'To Do'
    DONE = 'Done'
    DOING = 'Doing'

done_list_id = os.getenv('DONE_LIST_ID')

class Item:
    def __init__(self, id, title, status=ItemStatus.TO_DO):
        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def from_mongo_document(cls, doc):
        return Item(doc['_id'], doc['name'], ItemStatus(doc['status']))