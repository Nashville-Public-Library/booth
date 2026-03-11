from pathlib import Path

from flask import render_template, request
import requests

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
    return render_template("assets_folder.html", files=files, folder=folder)

@app.route("/assets/folder/<folder>/feed", methods=['POST'])
def assets_folder_feed(folder):
    url: str = f"https://assets.library.nashville.gov/talkinglibrary/shows/{folder}/feed.xml"
    request = requests.get(url)
    feed = request.text
    return {"feed": feed}

@app.route("/assets/folder/<folder>/feed/edit", methods=["POST"])
def assets_folder_feed_edit(folder):
    try:
        json: dict = request.json
        feed = json.get("feed")
        path = Path(f"tmp/feeds/{folder}/feed.xml")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(feed)
        ssh = SSH()
        ssh.upload_file(folder=folder, file=path)
        path.unlink()
        return {"response": f"The RSS feed for {folder} has been updated"}
    except Exception as e:
        return {"response": e}