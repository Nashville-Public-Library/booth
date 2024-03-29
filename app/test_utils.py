mock_EVs = {
        'VIC_user': 'nothing',
        'VIC_password': 'nothing!'
    }
from unittest.mock import patch
with patch.dict('os.environ', mock_EVs):
    from app.stream.icecast import Icecast
    from app.booth.utils import check_banner, are_we_closed, is_holiday
    from app.booth.hours import hour1, hour2

def test_are_we_closed_1():
    assert type(are_we_closed()) == bool

def test_hour_1_1():
    assert type(hour1()) == str

def test_hour_2_1():
    assert type(hour2()) == str

def test_check_banner():
    assert type(check_banner()) == bool or str

def test_holiday_1():
    assert type(is_holiday()) == str or bool

def test_check_icecast_1():
    '''should return dict for JSON response to front end'''
    assert type(Icecast().now_playing) == dict

def test_check_icecast_2():
    '''parsing the JSON (dict)'''
    now_playing = Icecast().now_playing
    assert type(now_playing['title']) == str