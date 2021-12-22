import requests
from flask import session
from todo_app.flask_config import Config
from todo_app.data.item import Item

base_url = 'https://api.trello.com'
api_version = '1'

def base_params():
    return {'key': Config().api_key, 'token': Config().api_token}

def prepareUrlAndParams(endpoint, params):
    return f'{base_url}/{api_version}/{endpoint}/', base_params() | params


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
        f'list/{Config().todo_list_id}/cards', {'fields': 'name,idList'})
    todoItems = todoResponse.json()

    doneResponse = trello_get(
        f'list/{Config().done_list_id}/cards', {'fields': 'name,idList'})
    doneItems = doneResponse.json()

    return map_all_cards_to_items(todoItems + doneItems)


def get_item(id):
    items = get_items()
    return next((item for item in items if item.id == id), None)


def add_item(title):
    r = trello_post('cards', {'name': title, 'idList': Config().todo_list_id})
    trello_card = r.json()

    return Item.from_trello_card(trello_card)


def save_item(item):
    itemId = item['id']
    r = trello_put(f'cards/{itemId}', {'idList': Config().done_list_id})
    done_card = r.json()

    return Item.from_trello_card(done_card)
