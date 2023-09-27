from flask import render_template, request, make_response

from app import app
from app.utils import are_we_closed, check_banner
from app.booth.hours import hour1, hour2
from app.booth.icecast import icecast_now_playing
from app.booth.scrape import scrape

@app.route('/live')
def homepage():
    if are_we_closed():
        return render_template('closed.html')

    booth1, booth2, booth3, booth1_2, booth2_2, booth3_2 = scrape()
    
    return render_template('home.html', booth1=booth1, booth2=booth2, booth3=booth3,\
        booth1_2=booth1_2, booth2_2=booth2_2, booth3_2=booth3_2, hour=hour1(), hour2=hour2(), banner=check_banner())

@app.route('/health')
def health_check():
    '''for AWS EB's health check'''
    if request.headers.get('User-Agent') == 'test':
        return 'la dee dah'
    return "<div style='font-size: 85pt; text-align: center;'>I AM WORKING FINE</div>" 

@app.route('/')
def dot():
    if are_we_closed():
        return render_template('closed.html')

    return render_template('land.html')

'''
just using this route for testing styles and such so we don't
need to run selenium every time we want to reload the page.
'''
@app.route('/test')
def testing():
    return render_template('home.html', booth1='Test Nobody', booth2='Test Nobody', booth3='Test Nobody',\
        booth1_2='Test Nobody', booth2_2='Test Nobody', booth3_2='Test Nobody', hour=hour1(), hour2=hour2(), banner=check_banner())

@app.route('/banner', methods=['GET', 'POST'])
def banner():
    if request.method == 'POST':
        password = request.form['password']
        message = request.form['message']
        if password == 'talk5874':
            with open('message.txt', 'w') as text:
                text.write(message)
            return render_template('banner.html', emoji='&#128077;', banner_text=check_banner()) # emoji = thumbs up
        else:
            return render_template('banner.html', emoji='&#128078;', banner_text=check_banner()) # emoji thumbs down
    return render_template('banner.html', banner_text=check_banner())

@app.route('/nowplaying')
def now_playing():
    icecast = {'nowPlaying': icecast_now_playing()}
    response = make_response(icecast)
    response.headers['customHeader'] = 'Darth Vader'
    response.status_code = 200
    response.content_type = 'application/json'
    response.access_control_allow_origin = '*'
    return response


# do something to explicitly handle HTTP errors so we don't get some general nginx page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404

@app.errorhandler(500)
def handle_exception(e):
    return render_template("broken.html", e=e), 500