from earthdaily import configs as conf
from earthdaily import create_app, db
import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        yield app
        


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_atm(client):
    resp = client.get(
        'http://localhost:5000/atms/'
    )
    assert resp.status_code == 200
    assert 0 <= len(json.loads(resp.data.decode('utf-8')))



def test_post_atm(client):
    resp = client.post(
        'http://localhost:5000/atms/',
        json={
        'geometry': { 
            'type': 'Point', 
            'coordinates': [49.2849777, -123.1189405] 
        },    
        'address': '1095 W Pender St, Vancouver, BC V6E 2M6',
        'provider': 'Manulife'
        }
    )

    assert resp.status_code == 201
    assert 0 <= len(json.loads(resp.data.decode('utf-8')))
