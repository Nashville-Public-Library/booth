from flask import Flask, render_template
from datetime import datetime
from testing import scrape, now

current_hour = datetime.now().strftime('%H')

application = Flask(__name__)

@application.route('/')
def homepage():
    if int(current_hour) < 9 or int(current_hour) > 16 :
        return render_template('closed.html')
    booth1, booth2, booth3 = scrape()
    return render_template('home.html', booth1=booth1, booth2=booth2, booth3=booth3, hour=now())

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