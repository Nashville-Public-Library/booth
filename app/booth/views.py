from flask import render_template, request, redirect, url_for

from app import app
from app.utils import are_we_closed, check_banner
from app.booth.hours import hour1, hour2
from app.booth.scrape import scrape

@app.route('/booth/live')
def homepage():
    if are_we_closed():
        return render_template('closed.html')

    booth1, booth2, booth3, booth1_2, booth2_2, booth3_2 = scrape()
    
    return render_template('booth.html', booth1=booth1, booth2=booth2, booth3=booth3,\
        booth1_2=booth1_2, booth2_2=booth2_2, booth3_2=booth3_2, hour=hour1(), hour2=hour2(), banner=check_banner())

@app.route('/health', methods=['GET', 'POST'])
def health_check():
    return "<div style='font-size: 85pt; text-align: center;'>I AM WORKING FINE</div>" 

@app.route('/booth')
def dot():
    if are_we_closed():
        return render_template('closed.html')

    return render_template('land.html')

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
        if password == 'talk5874':
            with open('message.txt', 'w') as text:
                text.write(message)
            return render_template('banner.html', emoji='&#128077;', banner_text=check_banner()) # emoji = thumbs up
        else:
            return render_template('banner.html', emoji='&#128078;', banner_text=check_banner()) # emoji thumbs down
    return render_template('banner.html', banner_text=check_banner())