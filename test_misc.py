import pytest

from application import application

@pytest.fixture
def client():
    application.config.update({'TESTING': True})

    with application.test_client() as client:
        yield client

'''
GET real GET routes
'''

def test_home(client):
    '''home/landing route'''
    resp = client.get('/')
    assert resp.status_code == 200

def test_live(client):
    '''
    Home route forwards here, the main page. 
    This calls the selenium script, which can take a while,
    so don't be alarmed if it takes 10+ seconds to run this test.
    '''
    resp = client.get('/live')
    assert resp.status_code == 200

def test_banner(client):
    response = client.get('/banner')
    assert response.status_code == 200

'''
GET non-GET routes
'''

def test_fake_url(client):
    '''non routes should return 404'''
    response = client.get('/maaah')
    assert response.status_code == 404

'''
POST real POST routes
'''

def test_banner_post(client):
    '''this is NOT testing whether the credentials are correct! only if the post request is formatted correctly'''
    response = client.post('/banner', data={"user": "","message": "",})
    assert response.status_code == 200

def test_banner_post_no_data(client):
    '''should fail if form data is missing'''
    response = client.post('/banner')
    assert response.status_code == 400

'''
POST non-POST routes
'''

def test_banner_post_no_data(client):
    '''should fail for non-POST routes'''
    response = client.post('/')
    assert response.status_code == 405