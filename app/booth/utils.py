from datetime import datetime

import holidays
import requests


def is_holiday():
    '''returns None if not a holiday'''
    holiday = holidays.US()
    today = datetime.now().strftime('%Y-%m-%d') # YYYY-MM-DD
    return holiday.get(today)

def are_we_closed() -> bool:
    '''if today is not a weekday or time is before x or after y, return True'''
    current_hour = datetime.now().strftime('%H')
    current_hour = int(current_hour)

    current_day = datetime.now().strftime('%a')
    weekend = ['Sat', 'Sun']

    if current_hour < 8 or current_hour > 16:
        return True

    if current_day in weekend:
        return True
    
    if is_holiday() != None:
        return True
    
    return False

def check_banner():
    banner = open('message.txt', 'r')
    banner = banner.read()

    if banner == '':
        banner == False
        
    return banner

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