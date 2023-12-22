import os
import xml.etree.ElementTree as ET

import requests

from app.ev import EV

def get_tree_from_icecast() -> str:
    icecast_URL = 'http://npl.streamguys1.com:/admin/stats.xml'
    ev = EV()

    tree = requests.get(icecast_URL, auth=(ev.icecast_user, ev.icecast_pass))
    if tree.status_code == 200:
        return tree.text
    else: return 'hmmmmm'

def parse_icecast_tree() -> str:
    tree = get_tree_from_icecast()
    tree = ET.fromstring(tree)
    mountpoints = tree.findall('source')
    for mount in mountpoints:
        if mount.get('mount') == '/live':
            now_playing = mount.find('yp_currently_playing')
            return now_playing.text

def icecast_now_playing():
    return parse_icecast_tree()
