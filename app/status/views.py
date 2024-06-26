from flask import render_template

from app import app
from app.status.ping import ping, check_mounts, listeners, server_start, outgoing_kbitrate, user_agent_ip
from app.auth import requires_auth

@app.route('/status')
@requires_auth
def status():
        return render_template('status.html')

@app.route('/status/ping', methods=['POST'])
def ping_ip():
    icecast = ping(host='npl.streamguys1.com')
    wpln = ping(host='12.247.152.50')
    SGmetadata = ping(host='204.93.152.147')
    metro = ping(host='170.190.43.1')
    npl = ping(host='library.nashville.org')
    return {
        'icecast': icecast, 
        'wpln': wpln, 
        'SGmetadata': SGmetadata, 
        'metro': metro, 
        'npl': npl}

@app.route('/status/stream', methods=['POST'])
def stream():
    return {
         'mounts': check_mounts(), 
         'listeners': listeners(), 
         'serverStart': server_start(), 
         'outgoing_kbitrate': outgoing_kbitrate()
         }

@app.route('/status/useragent/<mount>', methods=['POST'])
def user_agent(mount):
     return {'userAgent': user_agent_ip(mount=mount)}