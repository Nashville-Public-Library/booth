from flask import render_template, request, make_response

import requests

from app import app
from app.booth.utils import are_we_closed, check_banner, get_weather
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
    return response

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

@app.route('/booth/weather', methods=['POST'])
def weather():
    return get_weather()