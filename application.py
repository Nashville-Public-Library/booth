'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

from flask import Flask, render_template
from datetime import datetime

from testing import scrape, hour1, hour2

application = Flask(__name__)

@application.route('/')
def homepage():
    current_hour = datetime.now().strftime('%H')
    if int(current_hour) < 8 or int(current_hour) > 16 :
        return render_template('closed.html')

    booth1, booth2, booth3, booth1_2, booth2_2, booth3_2 = scrape()
    
    return render_template('home.html', booth1=booth1, booth2=booth2, booth3=booth3,\
        booth1_2=booth1_2, booth2_2=booth2_2, booth3_2=booth3_2, hour=hour1(), hour2=hour2())

@application.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@application.errorhandler(500)
def handle_exception(e):
    # pass through HTTP errors
    # if isinstance(e, HTTPException):
    #     return e

    # now you're handling non-HTTP exceptions only
    return render_template("broken.html", e=e), 500

if __name__ == '__main__':
    application.run()