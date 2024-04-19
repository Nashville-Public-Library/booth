from flask import render_template, request
import requests

from app import app
from app.status.ping import ping, check_mounts, listeners

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/status/ping', methods=['POST'])
def ping_ip():
    streamGuys = ping(host='npl.streamguys1.com')
    wpln = ping(host='12.247.152.50')
    SGmetadata = ping(host='204.93.152.147')
    metro = ping(host='170.190.43.1')
    return {'streamGuys': streamGuys, 'wpln': wpln, 'SGmetadata': SGmetadata, 'metro': metro}

@app.route('/status/stream', methods=['POST'])
def stream():
    return {'mounts': check_mounts(), 'listeners': listeners()}