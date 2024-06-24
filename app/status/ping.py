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
    '''
    I hate these try/except blocks, too. I tried iterating through all the elements of each source mount,
    but I just couldn't get it working. The Problem is the "name" for the source is not in the element.text attribute.
    you have to use element.get('source') to get the name. So that messes up the loop and I tried for hours but
    couldn't get it working. So just grab the few elements we actually need manually like this:
    '''
    for mount in mountpoints:
        try: 
            stream_start = mount.find("stream_start").text
        except:
            stream_start = '-'

        try: 
            listeners = mount.find("listeners").text
        except:
            listeners = "-"

        try:
            outgoing_kbitrate = mount.find("outgoing_kbitrate").text
        except:
            outgoing_kbitrate = "-"

        try: 
            title = mount.find('title').text
        except:
            title = "-"

        try:
            metadata_updated = mount.find("metadata_updated").text
        except:
            metadata_updated = "-"
        
        mount_list.append({"mount": 
                {"name": mount.get('mount'),
                "stream_start": stream_start,
                "listeners": listeners,
                "outgoing_kbitrate": outgoing_kbitrate,
                "title": title,
                "metadata_updated": metadata_updated
                }
                })


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
    return server_start

def outgoing_kbitrate():
    icecast_URL = "http://npl.streamguys1.com:/admin/stats.xml"
    ev = EV()
    tree = requests.get(icecast_URL, auth=(ev.icecast_user, ev.icecast_pass))
    tree = tree.text
    tree = ET.fromstring(tree)
    bitrate = tree.find('outgoing_kbitrate').text
    return bitrate

def user_agent_ip(mount):
    icecast_URL = f"http://npl.streamguys1.com:/admin/listclients?mount=/{mount}"
    ev = EV()
    tree = requests.get(icecast_URL, auth=(ev.icecast_user, ev.icecast_pass))
    tree = tree.text
    tree = ET.fromstring(tree)
    mountpoint = tree.find('source')
    try:
        agents = []
        listeners = mountpoint.findall('listener')
        for listener in listeners:
            user_agent = listener.find('UserAgent').text
            print(user_agent)
            agents.append(user_agent)
        return agents
    except:
        return []