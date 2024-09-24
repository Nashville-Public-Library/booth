from datetime import datetime

import holidays
import requests


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

def check_banner():
    banner = open('message.txt', 'r')
    banner = banner.read()
        
    return banner

def bannerColor():
    color = open('bannerColor.txt', 'r')
    color = color.read()
    
    return color

def get_weather():
    url = 'https://api.weather.gov/gridpoints/OHX/50,57/forecast/hourly'
    header = {'User-Agent': 'Darth Vader'}  # usually helpful to identify yourself
    request = requests.get(url=url, headers=header)
    try:
        weather = request.json()

        temp = weather['properties']['periods'][0]['temperature']

        forcast = weather['properties']['periods'][0]['shortForecast']

        chance_of_rain = weather['properties']['periods'][0]['probabilityOfPrecipitation']['value']

        photo:str = weather['properties']['periods'][0]['icon']
        photo = photo.replace('medium', 'small')
        photo = photo.replace(',0', '') #seems to be an error with API...

        response = {'temp': temp, 'photo': photo, 'forcast': forcast, 'chance_of_rain': chance_of_rain}
    except:
        response = 'failed', 500
    return response

def get_weather_alert():
    url = "https://api.weather.gov/alerts/active/zone/TNC037"
    header = {'User-Agent': 'Darth Vader'}  # usually helpful to identify yourself
    response = requests.get(url=url, headers=header)
    try:
        alert = response.json()
        alert = alert["features"][0]["properties"]["headline"]
        response = {"alert": alert}
    except:
        response = 'failed', 500
    return response