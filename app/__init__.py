'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

from flask import Flask

app = Flask(__name__)

from app.booth import views
from app.misc import views
from app.stream import views