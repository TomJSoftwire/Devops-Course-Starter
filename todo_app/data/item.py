import os

done_list_id = os.getenv('DONE_LIST_ID')

class Item:
    def __init__(self, id, title, status='To Do'):
        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def from_trello_card(cls, card):
        print(card)
        if(card['idList'] == done_list_id):
            return cls(card['id'], card['name'], 'Done')

        return cls(card['id'], card['name'], 'To Do')