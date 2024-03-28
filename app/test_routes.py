import pytest
from unittest.mock import patch

from app import app
from flask.testing import FlaskClient

env_vars = {
        'VIC_user': 'nothing',
        'VIC_password': 'mocked_value2'
    }

@pytest.fixture
def client():
    app.testing = True
    with patch.dict('os.environ', env_vars):
        client =  app.test_client()
        yield client
        
        # one of the tests writes a banner message. erase it.
        with open('message.txt', 'w') as banner:
            banner = banner.write('')

'''
GET real GET routes
'''

def test_home_get_1(client: FlaskClient):
    '''home/landing route'''
    resp = client.get('/')
    assert resp.status_code == 200

def test_banner_get_1(client: FlaskClient):
    response = client.get('/booth/banner')
    assert response.status_code == 200

'''
GET non-GET routes
'''

def test_booth_data_1(client: FlaskClient):
    '''post only'''
    response = client.get('/booth/data')
    assert response.status_code == 405

def test_fake_url_1(client: FlaskClient):
    '''non routes should return 404 no matter the request type'''
    response = client.get('/maaah')
    assert response.status_code == 404

def test_fake_url_2(client: FlaskClient):
    '''we always want to include '404' somewhere on the page, for clarity to user'''
    response = client.get('/maaah')
    assert '404' in response.text

def test_stream_get_1(client: FlaskClient):
    response = client.get('/stream')
    assert response.status_code == 405

def test_twilio_get_1(client: FlaskClient):
    response = client.get('/twilio')
    assert response.status_code == 405

'''
POST real POST routes
'''

def test_banner_post(client: FlaskClient):
    '''this is NOT testing whether the credentials are correct! only if the post request is formatted correctly'''
    response = client.post('/booth/banner', data=
                           {"password": "something",
                            "message": "something",
                            })
    assert response.status_code == 200

def test_banner_post_no_data(client: FlaskClient):
    '''should fail if form data is missing'''
    response = client.post('/booth/banner')
    assert response.status_code == 400

def test_banner_post_missing_data(client: FlaskClient):
    '''should fail if SOME form data is missing'''
    response = client.post('/booth/banner', data={"user": ""})
    assert response.status_code == 400

def test_banner_message(client: FlaskClient):
    from app.booth.utils import check_banner
    message = "some message here"
    response = client.post('/booth/banner', data=
                           {"password": "talk5874",
                            "message": message,
                            })
    assert check_banner() == message

def test_stream_post_1(client: FlaskClient):
    response = client.post('/stream')
    assert response.status_code == 200

def test_stream_post_2(client: FlaskClient):
    response = client.post('/stream')
    assert response.content_type == 'application/json'

def test_weather_post_1(client: FlaskClient):
    response = client.post('/booth/weather')
    assert response.status_code == 200

def test_weather_post_2(client: FlaskClient):
    response = client.post('/booth/weather')
    assert response.content_type == 'application/json'

def test_twilio_post_1(client: FlaskClient):
    response = client.post('/twilio')
    assert response.status_code == 200

def test_twilio_post_2(client: FlaskClient):
    response = client.post('/twilio')
    assert 'text/html' in response.content_type

'''
POST non-POST routes
'''

def test_home_post_1(client: FlaskClient):
    '''should fail for non-POST routes'''
    response = client.post('/')
    assert response.status_code == 405

def test_booth_post_1(client: FlaskClient):
    '''should fail for non-POST routes'''
    response = client.post('/booth')
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
    with patch.dict('os.environ', env_vars):
        from app.stream.icecast import Icecast
        assert type(Icecast().now_playing) == dict