"""
Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
Use of this software is governed by the license that can be
found in LICENSE file in the source repository.
"""

from fastapi.testclient import TestClient

from smighty.app.consts import APP_INITIALIZED_MESSAGE, APP_INITIALIZED_MESSAGE_HTML
from smighty.app.main import app


def test_root():
    client = TestClient(app)

    # Test with accept header as 'text/html'
    response = client.get('/', headers={'accept': 'text/html'})
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert response.text == APP_INITIALIZED_MESSAGE_HTML

    # # Test with accept header as other than 'text/html'
    response = client.get('/', headers={'accept': '*/*'})
    assert response.status_code == 200
    assert 'application/json' in response.headers['content-type']
    assert response.json() == {'message': APP_INITIALIZED_MESSAGE}
