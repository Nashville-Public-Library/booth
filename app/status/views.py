from flask import render_template, request

from app import app
from app.status.ping import ping, Icecast
from app.auth import requires_auth

@app.route('/status')
@requires_auth
def status():
        return render_template('status.html')

@app.route('/status/ping', methods=['POST'])
@requires_auth
def ping_ip():
    host: dict = request.get_json()
    host = host.get("host")
    pingable = ping(host=host)
    return {"result": pingable}

@app.route('/status/stream', methods=['POST'])
@requires_auth
def stream():
    icecast = Icecast()
    return {
         'mounts': icecast.check_mounts(), 
         'listeners': icecast.listeners(), 
         'serverStart': icecast.server_start(), 
         'outgoing_kbitrate': icecast.outgoing_kbitrate()
         }

@app.route('/status/useragent/<mount>', methods=['POST'])
# @requires_auth
def user_agent(mount):
     icecast = Icecast()
     return {'userAgent': icecast.user_agent_ip(mount=mount)}