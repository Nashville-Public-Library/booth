from flask import send_from_directory, render_template, make_response
import time

from app import app
from app.pwa.pod import Podcast

VERSION = "0.3.7"

@app.route('/pwa', methods=['GET'])
def pwa():
    return app.send_static_file("pwa/pages/index.html")

@app.route('/pwa/version', methods=['POST'])
def version():
    time.sleep(.4)
    return {"version": VERSION}

@app.route('/sw.js')
def serve_sw():
    response = make_response(render_template("sw.js", version=VERSION))
    response.headers["Content-Type"] = "application/javascript"
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.route('/pwa/podcasts', methods=['POST'])
def podcasts():
    shows = ("aarp", "able", "aroundworld", "atlantic", "bookpage", "checklist", "community", "consumer", "diabeties", "discover",
             "economist", "entertainment", "eyes", "fortune", "historical", "hourshortstories", "independent", "ledger", "lgbt",
             "mens", "moneytalk", "nationalgeo", "newsweek", "newyorker", "nyt", "opinion", "people", "pet", "poetry", "prevention",
             "readersdigest", "rollingstone", "scene", "science", "smithsonian", "sports", "tennessean", "time", "town", "vanity",
             "wired", "woman", "wsj")
    return {"podcasts": shows}

@app.route('/pwa/podcasts/info/<podcast>', methods=['POST'])
def podcasts_info(podcast):
    try:
        pod = Podcast(show=podcast)
        pod = pod.to_client()

        return render_template("pwa/podcast-individual.html", pod=pod)  
    except:
        return "", 500