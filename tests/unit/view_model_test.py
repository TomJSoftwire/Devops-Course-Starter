from todo_app.data.item import Item, ItemStatus
from todo_app.view_model import ViewModel
from todo_app.user import User

item_1 = Item('item_1', 'title_1', ItemStatus.TO_DO)
item_2 = Item('item_1', 'title_1', ItemStatus.TO_DO)
item_3 = Item('item_1', 'title_1', ItemStatus.DONE)
item_4 = Item('item_1', 'title_1', ItemStatus.DOING)

test_items = [item_1, item_2, item_3, item_4]

test_view_model = ViewModel(test_items, User('id'))


def test_to_do_items():
    result = test_view_model.todo_items

    assert result == [item_1, item_2]


def test_done_items():
    result = test_view_model.done_items

    assert result == [item_3]


def test_doing_items():
    result = test_view_model.doing_items

    assert result == [item_4]
