import xml.etree.ElementTree as ET
import os
import subprocess
import time

import ipinfo
import requests

from app.ev import EV

geo_cache:dict = {}

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

def geolocation(ip: str):
    '''
    the service we use to retreive this data rate limits us. since IP addresses
    tend not to change too much, we can safely cache the values. We're
    only caching to a global variable, so every time you restart the program (redeploy),
    the cache is emptied.
    '''
    try:
        token = EV().IPInfoToken
        if ip in geo_cache:
            return geo_cache.get(ip)
        handler = ipinfo.getHandler(token)
        details = handler.getDetails(ip)
        location = f"{details.city} ({details.region})"
        geo_cache.update({ip: location})
        return location
    except:
        # if we've exceeded our request limit for the month
        return "geolocation?"

class Icecast:
    def __init__(self) -> None:
        self.icecast_URL = "http://npl.streamguys1.com:/admin/stats.xml"
        self.ev = EV()
        self.icecast_tree = self.get_tree()
        self.mounts = self.check_mounts()
        self.listeners = self.get_listeners()
        self.server_start = self.get_server_start()
        self.outgoing_kbitrate = self.get_outgoing_kbitrate()

    def get_tree(self) -> ET.ElementTree:
        tree = requests.get(self.icecast_URL, auth=(self.ev.icecast_user, self.ev.icecast_pass))
        tree = tree.text
        tree = ET.fromstring(tree)
        return tree

    def check_mounts(self) -> list:
        mount_list = []
        tree = self.icecast_tree
        mountpoints = tree.findall('source')
        # Unfortunately not all mounts return the same data.
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
                incoming_bitrate = mount.find("incoming_bitrate").text
                incoming_bitrate = round(int(incoming_bitrate)/1000, 0)
            except:
                incoming_bitrate = "-"

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

            try:
                listenurl = mount.find("listenurl").text
            except:
                listenurl = "-"
            
            mount_list.append( 
                    {"name": mount.get('mount'),
                    "stream_start": stream_start,
                    "listeners": listeners,
                    "incoming_bitrate": incoming_bitrate,
                    "outgoing_kbitrate": outgoing_kbitrate,
                    "title": title,
                    "metadata_updated": metadata_updated,
                    "listenurl": listenurl
                    }
                    )


        return mount_list

    def get_listeners(self) -> str:
        tree = self.icecast_tree
        listeners = tree.find('listeners').text
        return listeners

    def get_server_start(self) -> str:
        tree = self.icecast_tree
        server_start = tree.find('server_start').text
        return server_start

    def get_outgoing_kbitrate(self) -> str:
        tree = self.icecast_tree
        bitrate = tree.find('outgoing_kbitrate').text
        return bitrate

    def user_agent_ip(self, mount) -> list:
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
                geo = geolocation(ip=IP_address)

                user_agent = listener.find('UserAgent').text

                connected = listener.find("Connected").text
                connected = str(round(int(connected) / 60, 1)) # convert to minutes, round to one decimal

                agents.append(f" {IP_address} • {geo} • {user_agent} • {connected} minutes")
            return agents
        except:
            return agents