import requests
from flask import session
from flask_config import Config
from data.item import Item

base_url = 'https://api.trello.com'
api_version = '1'

def base_params():
    return {'key': Config().api_key, 'token': Config().api_token}

def prepareUrlAndParams(endpoint, params):
    return f'{base_url}/{api_version}/{endpoint}/', {**base_params(), **params}


def trello_get(endpoint, params):
    return requests.get(*prepareUrlAndParams(endpoint, params))


def trello_post(endpoint, params):
    return requests.post(*prepareUrlAndParams(endpoint, params))


def trello_put(endpoint, params):
    return requests.put(*prepareUrlAndParams(endpoint, params))

def trello_delete(endpoint, params):
    url, params = prepareUrlAndParams(endpoint, params)
    return requests.delete(url, params=params)




def map_all_cards_to_items(cards):
    items = []
    for card in cards:
        items.append(Item.from_trello_card(card))
    return items

def get_list_ids():
    board_lists = trello_get(f'board/{Config().board_id}/lists', {}).json()

    todo_list_id = [x['id'] for x in board_lists if x['name'] == 'To Do'][0]
    done_list_id = [x['id'] for x in board_lists if x['name'] == 'Done'][0]

    return todo_list_id, done_list_id

def get_items():
    todo_list_id, done_list_id = get_list_ids()

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
    todo_list_id, _ = get_list_ids()
    r = trello_post('cards', {'name': title, 'idList': todo_list_id})
    trello_card = r.json()

    return Item.from_trello_card(trello_card)


def save_item(item):
    itemId = item['id']
    _, done_list_id = get_list_ids()
    r = trello_put(f'cards/{itemId}', {'idList': done_list_id})
    done_card = r.json()

    return Item.from_trello_card(done_card)

def create_todo_board():
    try:
        r = trello_post(f'boards', {'name': 'app_e2e_test_board', 'idOrganization': Config().organisation_id })
        response = r.json()
        return response['id']
    except Exception as e:
        print('failed to create board')
        raise Exception(e)

def delete_todo_board(boardId):
    r = trello_delete(f'boards/{boardId}', {})