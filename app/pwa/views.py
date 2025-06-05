from flask import render_template, request, send_from_directory

import requests

from app import app

@app.route('/pwa', methods=['GET'])
def pwa():
    return app.send_static_file("pwa/pages/index.html")

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

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
    base_URL = "https://assets.library.nashville.org/talkinglibrary/shows/" + podcast + "/"
    feed = base_URL + "feed.xml"
    image = base_URL + "image.jpg"

    return {"feed": feed, "image": image}