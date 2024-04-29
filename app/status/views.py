from functools import wraps

from flask import render_template, request, Response

from app import app
from app.ev import EV
from app.status.ping import ping, check_mounts, listeners

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'whoops, you must supply credentials', 
    401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(mah):
    """A decorator function that wraps other routes to check authentication"""
    @wraps(mah)
    def decorated():
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if type(ip) == tuple:
             if ip[0] in ('170.190.43.1', '127.0.0.1'):
                return f"first. type(ip): {type(ip)}, ip: {ip}, ip[0]: {ip[0]}"
        if ip == '170.190.43.1' or ip == '127.0.0.1':
             print(type(ip))
             return f"second. type(ip): {type(ip)}, ip: {ip}, ip[0]: {ip[0]}"
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        a = type(ip)
        return f"third. type(ip): {a}, ip: {ip}, ip[0]: {ip[0]}"
    return decorated

def check_auth(username: str, password: str):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username.lower() == 'admin' and password.lower() == EV().BF_pass

@app.route('/status')
@requires_auth
def status():
        return render_template('status.html')

@app.route('/del')
@requires_auth
def delete():
        return request.headers.get('X-Forwarded-For', request.remote_addr)

@app.route('/status/ping', methods=['POST'])
def ping_ip():
    icecast = ping(host='npl.streamguys1.com')
    wpln = ping(host='12.247.152.50')
    SGmetadata = ping(host='204.93.152.147')
    metro = ping(host='170.190.43.1')
    return {'icecast': icecast, 'wpln': wpln, 'SGmetadata': SGmetadata, 'metro': metro}

@app.route('/status/stream', methods=['POST'])
def stream():
    return {'mounts': check_mounts(), 'listeners': listeners()}