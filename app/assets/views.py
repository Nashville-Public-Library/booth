from flask import render_template

from app import app
from app.assets.ssh import SSH

@app.route("/assets")
def assets():
    ssh = SSH()
    folders = ssh.get_folders()
    return render_template("assets_overview.html", folders=folders)

@app.route("/assets/folder/<folder>")
def assets_folder(folder):
    ssh = SSH()
    files = ssh.get_items_in_folder(folder=folder)
    return render_template("assets_folder.html", files=files)