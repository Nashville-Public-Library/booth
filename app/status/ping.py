import xml.etree.ElementTree as ET
import os
import subprocess

import requests

from app.ev import EV

def ping(host):
    param = '-n' if 'nt' in os.name.lower() else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def check_mounts():
    mount_list = []
    icecast_URL = "http://npl.streamguys1.com:/admin/stats.xml"
    ev = EV()
    tree = requests.get("http://npl.streamguys1.com:/admin/stats.xml", auth=(ev.icecast_user, ev.icecast_pass))
    tree = tree.text
    tree = ET.fromstring(tree)
    mountpoints = tree.findall('source')
    for mount in mountpoints:
        mount_list.append(mount.get('mount'))
    return mount_list

def listeners():
    icecast_URL = "http://npl.streamguys1.com:/admin/stats.xml"
    ev = EV()
    tree = requests.get("http://npl.streamguys1.com:/admin/stats.xml", auth=(ev.icecast_user, ev.icecast_pass))
    tree = tree.text
    tree = ET.fromstring(tree)
    listeners = tree.find('listeners').text
    return listeners