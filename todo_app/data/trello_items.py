import requests
from flask import session
import os

base_url = 'https://api.trello.com'
api_version = '1'
api_key = os.getenv('TRELLO_KEY')
api_token = os.getenv('TRELLO_TOKEN')

todo_list_id = '619e23e145c81b50c4cb9c08'
done_list_id = '619e23e145c81b50c4cb9c0a'

base_params = {'key': api_key, 'token': api_token}


def build_url(endpoint):
    return f'{base_url}/{api_version}/{endpoint}/'

def prepareUrlAndParams(endpoint, params):
    return build_url(endpoint), base_params | params

def trello_get(endpoint, params):
    return requests.get(*prepareUrlAndParams(endpoint, params))


def trello_post(endpoint, params):
    return requests.post(*prepareUrlAndParams(endpoint, params))


def trello_put(endpoint, params):
    return requests.put(*prepareUrlAndParams(endpoint, params))


def map_card_to_item(card):
    return {'id': card['id'], 'title': card['name'], 'status': 'Not Started'}


def map_all_cards_to_items(cards):
    items = []
    for card in cards:
        items.append(map_card_to_item(card))
    return items


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    r = trello_get(f'list/{todo_list_id}/cards', {'fields': 'name'})
    items = r.json()
    return map_all_cards_to_items(items)


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == id), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    r = trello_post('cards', {'name': title, 'idList': todo_list_id})
    trello_card = r.json()

    return map_card_to_item(trello_card)


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    itemId = item['id']
    r = trello_put(f'cards/{itemId}', {'idList': done_list_id})
    done_card = r.json()

    return map_card_to_item(done_card)
