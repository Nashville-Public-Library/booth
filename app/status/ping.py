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
    tree = requests.get(icecast_URL, auth=(ev.icecast_user, ev.icecast_pass))
    tree = tree.text
    tree = ET.fromstring(tree)
    mountpoints = tree.findall('source')
    for mount in mountpoints:
        try:
            mount_list.append({"mount": {"name": mount.get('mount'),
                           "stream_start": mount.find("stream_start").text,
                           "listeners": mount.find("listeners").text,
                           "title": mount.find('title').text,
                           "metadata_updated": mount.find("metadata_updated").text}})
        except: #some mountpoints may not have 'title' or 'metadata_updated' tags, which could cause an error
            mount_list.append({"mount": {"name": mount.get('mount'), 
                            "stream_start": mount.find("stream_start").text,
                            "listeners": mount.find("listeners").text,
                            "title": '-',
                            "metadata_updated": "-"}})


    return mount_list

def listeners():
    icecast_URL = "http://npl.streamguys1.com:/admin/stats.xml"
    ev = EV()
    tree = requests.get(icecast_URL, auth=(ev.icecast_user, ev.icecast_pass))
    tree = tree.text
    tree = ET.fromstring(tree)
    listeners = tree.find('listeners').text
    return listeners

def server_start():
    icecast_URL = "http://npl.streamguys1.com:/admin/stats.xml"
    ev = EV()
    tree = requests.get(icecast_URL, auth=(ev.icecast_user, ev.icecast_pass))
    tree = tree.text
    tree = ET.fromstring(tree)
    server_start = tree.find('server_start').text
    print(server_start)
    return server_start