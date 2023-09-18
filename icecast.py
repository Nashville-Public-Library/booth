import xml.etree.ElementTree as ET
import os

import requests

def get_tree_from_icecast():
    icecast_user = os.environ['icecast_user']
    icecast_pass = os.environ['icecast_pass']
    icecast_URL = 'http://npl.streamguys1.com:/admin/stats.xml'

    tree = requests.get(icecast_URL, auth=(icecast_user, icecast_pass))
    if tree.status_code == 200:
        return tree.text
    else: return 'hmmmmm'

def parse_icecast_tree():
    tree = get_tree_from_icecast()
    tree = ET.fromstring(tree)
    mountpoints = tree.findall('source')
    for mount in mountpoints:
        if mount.get('mount') == '/live':
            now_playing = mount.find('yp_currently_playing')
            return now_playing.text

def icecast_now_playing():
    return parse_icecast_tree()
