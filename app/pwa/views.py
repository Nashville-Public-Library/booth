from flask import send_from_directory, render_template

from app import app
from app.pwa.pod import Podcast

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
    pod = Podcast(show=podcast)
    pod = pod.to_client()

    return render_template("podcast-individual.html", pod=pod)  