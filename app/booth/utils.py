from datetime import datetime

from diskcache import Cache
import holidays
import requests

weather_cache = Cache("weather_cache")

def is_holiday():
    '''returns None if not a holiday'''
    holiday: dict = holidays.US()
    today = datetime.now().strftime('%Y-%m-%d') # YYYY-MM-DD
    return holiday.get(today)

def is_weekend() -> bool:
    current_day = datetime.now().strftime('%a')
    weekend = ['Sat', 'Sun']
    
    if current_day in weekend:
        return True

def date_is_weekend(date: datetime) -> bool:
    day = date.strftime("%a")
    weekend = ['Sat', 'Sun']
    if day in weekend:
        return True
    
def is_outside_business_hours() -> bool:
    current_hour = datetime.now().strftime('%H')
    current_hour = int(current_hour)

    if current_hour < 8 or current_hour > 16:
        return True

def are_we_closed() -> bool:    
    if is_holiday() != None:
        return True
    
    if is_weekend():
        return True
    
    if is_outside_business_hours():
        return True
    
    return False

def get_weather() -> dict:
    forecast = check_weather_cache("forecast")
    if forecast:
        return forecast
    
    url = 'https://api.weather.gov/gridpoints/OHX/50,57/forecast/hourly'
    header = {'User-Agent': 'Darth Vader'}  # usually helpful to identify yourself
    request = requests.get(url=url, headers=header)
    try:
        weather = request.json()

        temp = weather['properties']['periods'][0]['temperature']
        forecast = weather['properties']['periods'][0]['shortForecast']
        chance_of_rain = weather['properties']['periods'][0]['probabilityOfPrecipitation']['value']

        response = {'temp': temp, 'forecast': forecast, 'chance_of_rain': chance_of_rain}
        save_to_cache(key="forecast", value=response)
    except:
        response = 'failed', 500
    return response

def get_weather_alert() -> dict:
    url = "https://api.weather.gov/alerts/active/zone/TNC037"
    header = {'User-Agent': 'Darth Vader'}  # usually helpful to identify yourself
    response = requests.get(url=url, headers=header)
    try:
        alert = response.json()
        alert = alert["features"][0]["properties"]["headline"]
        response = {"alert": alert}
    except:
        response = {"alert": None}
    return response

def check_weather_cache(key: str):
    result: str = weather_cache.get(key=key)
    return result

def save_to_cache(key: str, value: str):
    weather_cache.add(key=key, value=value, expire=120)