'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

from flask import Flask

from app.ev import EV

app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = EV().icecast_pass

from app.assets import views
from app.booth import views
from app.misc import views
from app.status import views
from app.stream import views
from app.upload import views