from flask import render_template, request, make_response

import requests

from app import app
from app.booth.utils import are_we_closed, check_banner
from app.booth.hours import hour1, hour2
from app.booth.scrape import get_scrape_and_filter

@app.route('/booth')
def dot():
    if are_we_closed():
        return render_template('closed.html')

    return render_template('booth.html', hour=hour1(), hour2=hour2(), banner=check_banner())

@app.route('/booth/data', methods=['POST'])
def homepage():
    response = make_response(get_scrape_and_filter())
    response = make_response(response)
    response.headers['customHeader'] = 'Darth Vader'
    response.status_code = 200
    response.content_type = 'application/json'
    response.access_control_allow_origin = '*'
    return response

@app.route('/health', methods=['GET', 'POST'])
def health_check():
    return "<div style='font-size: 85pt; text-align: center;'>I AM WORKING FINE</div>" 

@app.route('/booth/banner', methods=['GET', 'POST'])
def banner():
    if request.method == 'POST':
        password = request.form['password']
        message = request.form['message']
        message = message.strip()
        if password == 'talk5874':
            with open('message.txt', 'w') as text:
                text.write(message)
            return render_template('banner.html', emoji='&#128077;', banner_text=check_banner()) # emoji = thumbs up
        else:
            return render_template('banner.html', emoji='&#128078;', banner_text=check_banner()) # emoji thumbs down
    return render_template('banner.html', banner_text=check_banner())

@app.route('/booth/weather', methods=['GET', 'POST'])
def weather():
    request = requests.get('https://api.weather.gov/gridpoints/OHX/50,57/forecast/hourly')
    
    weather = request.json()
    temp = weather['properties']['periods'][0]['temperature']
    photo = weather['properties']['periods'][0]['icon']
    photo = photo.replace('medium', 'small')
    photo = photo.replace(',0', '') #seems to be an error with API...
    response = {'temp': temp, 'photo': photo}

    return response