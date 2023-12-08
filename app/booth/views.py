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
    # response = {'booth1_1': 'mah', 'booth2_1': 'mahh', 'booth3_1': 'mahhh', 'booth1_2': 'mahhhh', 'booth2_2': 'mahhh', 'booth3_2': 'mahhh'}
    response = make_response(response)
    response.headers['customHeader'] = 'Darth Vader'
    response.status_code = 200
    response.content_type = 'application/json'
    response.access_control_allow_origin = '*'
    print(response)
    return response

@app.route('/health', methods=['GET', 'POST'])
def health_check():
    return "<div style='font-size: 85pt; text-align: center;'>I AM WORKING FINE</div>" 

'''
just using this route for testing styles and such so we don't
need to run selenium every time we want to reload the page.
'''
@app.route('/booth/test')
def testing():
    return render_template('booth.html', booth1='Test Nobody', booth2='Test Nobody', booth3='Test Nobody',\
        booth1_2='Test Nobody', booth2_2='Test Nobody', booth3_2='Test Nobody', hour=hour1(), hour2=hour2(), banner=check_banner())

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

@app.route('/booth/weather')
def weather():
    request = requests.get('https://api.weather.gov/gridpoints/OHX/50,57/forecast')
    
    weather = request.json()
    temp = weather['properties']['periods'][0]['temperature']
    photo = weather['properties']['periods'][0]['icon']
    photo = photo.replace('medium', 'large')
    response = {'temp': temp, 'photo': photo}

    return response