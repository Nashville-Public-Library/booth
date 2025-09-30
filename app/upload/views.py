from datetime import datetime

from flask import render_template, request
import waifuvault
import io

from app import app
from app.ev import EV
from app.sql import SQL
from app.auth import require_auth

@app.route("/upload", methods=['GET'])
def upload():
    return render_template("upload.html")

@app.route("/upload/viewfiles", methods=["GET"])
@require_auth
def view_files():
    sql = SQL()
    files = sql.read_uploads()
    return render_template("view_upload_files.html", files=files)

@app.route("/upload/newfile", methods=["POST"])
def upload_to_server():
    json: dict = request.get_json() 
    if not json.get("password") == EV().VIC_user:
        return {"response": "bad password"}, 401
    try:
        # encrypt file on server
        waifuvault.file_update(token=json.get("token"), password=EV().VIC_user, previous_password=EV().VIC_user)

        timestamp = datetime.now().strftime("%b %d, %I:%M%p")
        SQL().write_uploads(filename=json.get("filename"), url=json.get("url"), token=json.get("token"), timestamp=timestamp)

        return {'response': "OK"}, 200
    except Exception as e: return {"response": "problem on server..."}, 500

@app.route("/upload/deletefile", methods=["DELETE"])
@require_auth
def delete_file():
    file:dict = request.get_json()
    file = file.get("filename")
    sql = SQL()
    sql.delete_uploads(filename=file)
    return {"response": "OK"}, 200

@app.route("/upload/setpassword")
def set_password():
    password = EV().VIC_user
    upload:dict = request.get_json()
    if upload.get("password") == password:
        waifuvault.file_update(token=upload.get("token"), password=EV().VIC_user)
        return {"response": "OK"}, 200
    return {"response": "bad password"}, 401

@app.route("/upload/checkpassword", methods=["POST"])
def check_password():
    password:dict = request.get_json()
    password = password.get("password")
    if password == EV().VIC_user:
        return {"response": "OK"}, 200
    return {"response": "bad password"}, 401

@app.route("/upload/uploads", methods=["POST"])
def uploads():
    sql = SQL()
    files = sql.read_uploads()
    return {"files": files}