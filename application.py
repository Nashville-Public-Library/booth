from cmath import e
from flask import Flask, render_template
from testing import scrape, now

application = Flask(__name__)

@application.route('/')
def homepage():
    booth1, booth2, booth3 = scrape()
    return render_template('home.html', booth1=booth1, booth2=booth2, booth3=booth3, hour=now())

if __name__ == '__main__':
    application.run(debug=True)