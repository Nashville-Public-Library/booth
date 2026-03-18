from pathlib import Path

from flask import render_template, request
from app.auth import require_auth

from app import app
from app.assets.ssh import SSH

@app.route("/assets")
@require_auth
def assets():
    folders = SSH().assets()
    return render_template("assets_overview.html", folders=folders)

@app.route("/assets/folder/<folder>")
@require_auth
def assets_folder(folder):
    try:
        files = SSH().assets_folder_folder(folder=folder)
        return render_template("assets_folder.html", files=files, folder=folder)
    except FileExistsError as e:
        return f"{e}", 400

@app.route("/assets/folder/feed", methods=['POST'])
@require_auth
def assets_folder_feed():
    response = SSH().assets_folder_feed(request_json=request)
    return response

@app.route("/assets/folder/feed/edit", methods=["POST"])
@require_auth
def assets_folder_feed_edit():
    try:
        response = SSH().assets_folder_feed_edit(request_json=request)
        return response
    except Exception as e:
        return {"response": f"Error uploading to server: {e}"}, 500

@app.route("/assets/folder/upload", methods=["PUT"])
@require_auth
def assets_folder_upload():
    try:
        response = SSH().assets_folder_upload(request_json=request)
        return response
    except Exception as e:
        return {"response": f"Error uploading to server: {e}"}, 500 

@app.route("/assets/folder/new", methods=["POST"])
@require_auth
def assets_folder_new():
    response = SSH().assets_folder_new(request_json=request)
    return response