from functools import wraps

from flask import request, redirect, session, url_for

from app.ev import EV

def require_auth_if_outside_metro(mah):
    '''these routes are not particularly sensitive'''
    @wraps(mah)
    def decorated(*args, **kwargs):
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')
        if ip[0] == '127.0.0.1' or ip[0].startswith("10.28."): # if developing locally or local IP
            return mah(*args, **kwargs)
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.path))
        return mah(*args, **kwargs)
    return decorated

def require_auth(mah):
    '''these routes should always require auth'''
    @wraps(mah)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.path))
        return mah(*args, **kwargs)
    return decorated

def check_auth(username: str, password: str) -> bool:
    """This function is called to check if a username /
    password combination is valid.
    """
    return username.lower() == 'admin' and password.lower() == EV().BF_pass