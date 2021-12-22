import requests
from flask import session
import os
from todo_app.data.item import Item

base_url = 'https://api.trello.com'
api_version = '1'
api_key = os.getenv('TRELLO_KEY')
api_token = os.getenv('TRELLO_TOKEN')

todo_list_id = os.getenv('TODO_LIST_ID')
done_list_id = os.getenv('DONE_LIST_ID')

base_params = {'key': api_key, 'token': api_token}

def prepareUrlAndParams(endpoint, params):
    return f'{base_url}/{api_version}/{endpoint}/', base_params | params


def trello_get(endpoint, params):
    return requests.get(*prepareUrlAndParams(endpoint, params))


def trello_post(endpoint, params):
    return requests.post(*prepareUrlAndParams(endpoint, params))


def trello_put(endpoint, params):
    return requests.put(*prepareUrlAndParams(endpoint, params))




def map_all_cards_to_items(cards):
    items = []
    for card in cards:
        items.append(Item.from_trello_card(card))
    return items


def get_items():
    todoResponse = trello_get(
        f'list/{todo_list_id}/cards', {'fields': 'name,idList'})
    todoItems = todoResponse.json()

    doneResponse = trello_get(
        f'list/{done_list_id}/cards', {'fields': 'name,idList'})
    doneItems = doneResponse.json()

    return map_all_cards_to_items(todoItems + doneItems)


def get_item(id):
    items = get_items()
    return next((item for item in items if item.id == id), None)


def add_item(title):
    r = trello_post('cards', {'name': title, 'idList': todo_list_id})
    trello_card = r.json()

    return Item.from_trello_card(trello_card)


def save_item(item):
    itemId = item['id']
    r = trello_put(f'cards/{itemId}', {'idList': done_list_id})
    done_card = r.json()

    return Item.from_trello_card(done_card)
