from flask import make_response, redirect

from app import app
from app.stream.icecast import icecast_now_playing

@app.route('/stream')
def now_playing():
    icecast = {'nowPlaying': icecast_now_playing()}
    response = make_response(icecast)
    response.headers['customHeader'] = 'Darth Vader'
    response.status_code = 200
    response.content_type = 'application/json'
    response.access_control_allow_origin = '*'
    return response

@app.route('/stream/livestream.mp3')
def livestream():
    return redirect('https://npl.streamguys1.com/live')