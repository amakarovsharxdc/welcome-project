def test_post_items(client, api):
    api.storage.tree.clear()
    response = client.post(
        '/items.json',
        json=[
            ("GET", "/api/v1/cluster/metrics"),
            ("POST", "/api/v1/cluster/{cluster}/plugins"),
            ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        'cluster': {
            'metrics': 'GET',
            'plugins': 'POST',
        },
    }

    response = client.post(
        '/items.json',
        json=[
            ("GET", "/api/v1/cluster/freenodes/list"),
            ("GET", "/api/v1/cluster/nodes"),
            ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
            ("POST", "/api/v1/cluster/{cluster}/plugins"),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        'cluster': {
            'metrics': 'GET',
            'plugins': 'POST',
            'freenodes': {
                'list': 'GET',
            },
            'nodes': 'GET',
        },
    }
