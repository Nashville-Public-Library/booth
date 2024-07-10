from flask import render_template, request

from app import app
from app.status.ping import ping, check_mounts, listeners, server_start, outgoing_kbitrate, user_agent_ip
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
    return {
         'mounts': check_mounts(), 
         'listeners': listeners(), 
         'serverStart': server_start(), 
         'outgoing_kbitrate': outgoing_kbitrate()
         }

@app.route('/status/useragent/<mount>', methods=['POST'])
# @requires_auth
def user_agent(mount):
     return {'userAgent': user_agent_ip(mount=mount)}