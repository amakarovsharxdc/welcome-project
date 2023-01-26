import pytest

from service.api import VerbAlreadyExists
from service.models import Item


@pytest.mark.parametrize('item, tree', [
    (
        Item('GET', '/'),
        {'': 'GET'},
    ),
    (
        Item('GET', '/a/b'),
        {'a': {'b': 'GET'}},
    ),
    (
        Item('GET', '/api/v1/a/b'),
        {'a': {'b': 'GET'}},
    ),
    (
        Item('GET', '/a/b/{c}'),
        {'a': {'b': 'GET'}},
    ),
    (
        Item('GET', '/a/{b}/c'),
        {'a': {'c': 'GET'}},
    ),
    (
        Item('GET', '/a/{b}/c/{d}'),
        {'a': {'c': 'GET'}},
    ),
])
def test_add_item(api, storage, item, tree):
    api.add_item(item)
    assert storage.tree == tree


def test_add_item_exception(api):
    api.add_item(Item('GET', '/a/b'))
    with pytest.raises(VerbAlreadyExists):
        api.add_item(Item('POST', '/a/b'))


def test_add_items(api, storage):
    api.add_items([
        Item('GET', '/a/b'),
        Item('GET', '/a/c'),
        Item('GET', '/d/e'),
    ])
    assert storage.tree == {
        'a': {'b': 'GET', 'c': 'GET'},
        'd': {'e': 'GET'},
    }


def test_get_tree(api, storage):
    storage.tree.update({'a': {'b': 'GET', 'c': 'GET'}})
    assert api.get_tree() == {'a': {'b': 'GET', 'c': 'GET'}}
