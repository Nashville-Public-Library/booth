import pytest

from app import app

@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client

'''
GET real GET routes
'''

def test_home_1(client):
    '''home/landing route'''
    resp = client.get('/booth')
    assert resp.status_code == 200
    assert 'booth' in resp.text

def test_home_2(client):
    '''booth assignments should always be present, unless we're closed, then closed should be there'''
    resp = client.get('/booth/live')
    assert 'booth' or 'closed' in resp.text

def test_banner(client):
    response = client.get('/booth/banner')
    assert response.status_code == 200

def test_stream_1(client):
    response = client.get('/stream')
    assert response.status_code == 200

def test_stream_2(client):
    response = client.get('/stream')
    assert response.content_type == 'application/json'

'''
GET non-GET routes
'''

def test_booth_data_1(client):
    response = client.get('/booth/data')
    assert response.status_code == 405

def test_fake_url_1(client):
    '''non routes should return 404'''
    response = client.get('/maaah')
    assert response.status_code == 404

def test_fake_url_2(client):
    '''we always want to include '404' somewhere on the page, for clarity to user'''
    response = client.get('/maaah')
    assert '404' in response.text

'''
POST real POST routes
'''

def test_banner_post(client):
    '''this is NOT testing whether the credentials are correct! only if the post request is formatted correctly'''
    response = client.post('/booth/banner', data=
                           {"password": "something",
                            "message": "something",
                            })
    assert response.status_code == 200

def test_banner_post_no_data(client):
    '''should fail if form data is missing'''
    response = client.post('/booth/banner')
    assert response.status_code == 400

def test_banner_post_missing_data(client):
    '''should fail if SOME form data is missing'''
    response = client.post('/booth/banner', data={"user": ""})
    assert response.status_code == 400

'''
POST non-POST routes
'''

def test_home_post_1(client):
    '''should fail for non-POST routes'''
    response = client.post('/booth')
    assert response.status_code == 405

def test_home_post_3(client):
    '''should fail for non-POST routes'''
    response = client.post('/stream')
    assert response.status_code == 405


'''MISC Functions'''

def test_are_we_closed_1():
    from app.booth.utils import are_we_closed
    assert type(are_we_closed()) == bool

def test_hour_1_1():
    from app.booth.hours import hour1
    assert type(hour1()) == str

def test_hour_2_1():
    from app.booth.hours import hour2
    assert type(hour2()) == str

def test_check_banner():
    from app.booth.utils import check_banner
    assert type(check_banner()) == bool or str

def test_check_icecast():
    from app.stream.icecast import icecast_now_playing
    assert type(icecast_now_playing()) == str