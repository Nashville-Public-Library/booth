from datetime import datetime

from flask import render_template, request, make_response

from app import app
from app.booth.utils import are_we_closed, check_banner, bannerColor, get_weather, get_weather_alert, is_holiday
from app.booth.hours import hour1, hour2
from app.booth.scrape import get_scrape_and_filter
from app.ev import EV
from app.auth import require_auth_if_outside_metro

@app.route('/booth')
@require_auth_if_outside_metro
def dot():
    if are_we_closed():
        return render_template('closed.html')
    if datetime.now().month == 12:
        return render_template('booth_xmas.html', hour=hour1(), hour2=hour2())
    return render_template('booth.html', hour=hour1(), hour2=hour2())

@app.route('/booth/schedule')
@require_auth_if_outside_metro
def schedule():
    return render_template('schedule.html')

@app.route('/booth/data', methods=['POST'])
@require_auth_if_outside_metro
def booth_data():
    try:
        json: dict = request.get_json() 
        date = datetime(day=int(json.get("day")), month=int(json.get("month")), year=int(json.get("year")))
    except:
        date = datetime.now() # today

    response = make_response(get_scrape_and_filter(date=date))
    return response

@app.route('/booth/banner', methods=['GET', 'POST'])
def banner():
    if request.method == 'POST':
        password = request.form['password']
        message = request.form['message']
        BannerColor = request.form['bannerColor']
        message = message.strip()
        if password == EV().BF_pass:
            with open('message.txt', 'w') as text:
                text.write(message)
            with open('bannerColor.txt', 'w') as color:
                color.write(BannerColor)
            return render_template('banner.html', emoji='&#128077;') # emoji = thumbs up
        else:
            return render_template('banner.html', emoji='&#128078;') # emoji thumbs down
    return render_template('banner.html')

@app.route('/booth/banner/content', methods=['POST'])
def banner_content():
    return {'banner': check_banner(), 'bannerColor': bannerColor()}

@app.route('/booth/weather', methods=['POST'])
def weather():
    return get_weather()

@app.route('/booth/weather/alert', methods=['POST'])
def weather_alert():
    return get_weather_alert()
    

@app.route('/booth/holiday', methods=['POST'])
def holiday():
    holiday = is_holiday()
    return {'holiday': holiday}
