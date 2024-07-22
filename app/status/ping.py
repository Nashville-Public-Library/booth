import xml.etree.ElementTree as ET
import os
import subprocess
import time

import requests

from app.ev import EV

def ping(host):
    param = '-n' if 'nt' in os.name.lower() else '-c'
    command = ['ping', param, '1', host]
    
    # keep the output quiet (varies depending on the OS) 
    if 'nt' in os.name.lower():
        command.extend(['>', 'nul', '2>&1'])
    else:
        command.extend(['>', '/dev/null', '2>&1'])

    # Join the command list into a single string for subprocess.call
    command_str = ' '.join(command)

    time.sleep(0.5)

    return subprocess.call(command_str, shell=True) == 0

class Icecast:
    def __init__(self) -> None:
        self.icecast_URL = "http://npl.streamguys1.com:/admin/stats.xml"
        self.ev = EV()
        self.icecast_tree = self.get_tree()

    def get_tree(self) -> ET.ElementTree:
        tree = requests.get(self.icecast_URL, auth=(self.ev.icecast_user, self.ev.icecast_pass))
        tree = tree.text
        tree = ET.fromstring(tree)
        return tree

    def check_mounts(self):
        mount_list = []
        tree = self.icecast_tree
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

    def listeners(self):
        tree = self.icecast_tree
        listeners = tree.find('listeners').text
        return listeners

    def server_start(self):
        tree = self.icecast_tree
        server_start = tree.find('server_start').text
        return server_start

    def outgoing_kbitrate(self):
        tree = self.icecast_tree
        bitrate = tree.find('outgoing_kbitrate').text
        return bitrate

    def user_agent_ip(self, mount):
        icecast_URL = f"http://npl.streamguys1.com:/admin/listclients?mount=/{mount}"
        tree = requests.get(icecast_URL, auth=(self.ev.icecast_user, self.ev.icecast_pass))
        tree = tree.text
        tree = ET.fromstring(tree)
        mountpoint = tree.find('source')
        agents = []
        try:
            listeners = mountpoint.findall('listener')
            for listener in listeners:
                IP_address = listener.find("IP").text

                user_agent = listener.find('UserAgent').text

                connected = listener.find("Connected").text
                connected = str(round(int(connected) / 60, 1)) # convert to minutes, round to one decimal

                agents.append(IP_address + " | " + user_agent + " | " + connected + " minutes")
            return agents
        except:
            return agents