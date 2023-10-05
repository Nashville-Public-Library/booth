import os

class EV():
    def __init__(self) -> None:
        self.icecast_user = os.environ['icecast_user']
        self.icecast_pass = os.environ['icecast_pass']