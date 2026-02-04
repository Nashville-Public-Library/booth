import os

class EV():
    def __init__(self) -> None:
        self.icecast_user = os.environ['icecast_user']
        self.icecast_pass = os.environ['icecast_pass']
        self.VIC_user = os.environ['VIC_user']
        self.VIC_pass = os.environ['VIC_password']
        self.BF_pass = os.environ['BF_pass']
        self.IPInfoToken = os.environ['IPInfoToken']
        self.mail_server_external = os.environ['mail_server_external']