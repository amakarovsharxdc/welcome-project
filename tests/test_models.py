from service.models import Item


def test_item():
    item = Item('GET', '/path')
    assert item.verb == 'GET'
    assert item.path == '/path'
