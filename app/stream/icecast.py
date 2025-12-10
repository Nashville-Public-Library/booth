import xml.etree.ElementTree as ET

from diskcache import Cache
import requests

from app.ev import EV

now_playing_cache = Cache("cache")

class Icecast:
    def __init__(self) -> None:
        self.icecast_URL = "http://npl.streamguys1.com:/admin/stats.xml"
        self.now_playing = self.get_now_playing()

    def get_tree_from_icecast(self) -> str:
        ev = EV()
        tree = requests.get(self.icecast_URL, auth=(ev.icecast_user, ev.icecast_pass))
        if tree.status_code == 200:
            return tree.text

    def parse_full_tree_for_live_mount(self) -> ET.ElementTree:
        tree = self.get_tree_from_icecast()
        tree = ET.fromstring(tree)
        mountpoints = tree.findall('source')
        for mount in mountpoints:
            if mount.get('mount') == '/live':
                return mount
    
    def parse_mount_for_elements(self) -> dict:
        '''
        This one is for the NPL website. PLEASE LEAVE AS-IS.
        If you need to extend functionality, please add new methods, 
        or else submit a patch to the NPL web team.
        '''
        mount = self.parse_full_tree_for_live_mount()
        try:
            yp_currently_playing = mount.find('yp_currently_playing').text
            title = mount.find('title').text
            metadata_updated = mount.find('metadata_updated').text
        except:
            yp_currently_playing = None
            title = None
            metadata_updated = None
        return {
            'yp_currently_playing': yp_currently_playing, 
            'title': title, 
            'metadata_updated': metadata_updated
            }

    def get_now_playing(self):
        '''If we have a cached value, return it. If not, make a call to Icecast, cache the response, then return it.'''
        try:
            cached = now_playing_cache["now_playing"]
            print("cached: " + str(cached))
            return cached
        except:
            new = self.parse_mount_for_elements()
            now_playing_cache.set(key="now_playing", value=new, expire=10)
            print("updating cache: " + str(new))
            return new