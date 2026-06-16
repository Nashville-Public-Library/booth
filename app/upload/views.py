from datetime import datetime
from pathlib import Path
import shutil

from flask import render_template, request, send_file, redirect
import requests
import waifuvault
from waifuvault import FileResponse

from app import app
from app.ev import EV
from app.sql import SQL
from app.auth import require_auth
from app.notify import send_mail_on_new_file_upload


@app.route("/upload", methods=['GET'])
def upload():
    return render_template("upload.html")

@app.route("/upload/viewfiles", methods=["GET"])
@require_auth
def view_files():
    sql = SQL()
    files = sql.read_uploads()
    return render_template("view_upload_files.html", files=files)

@app.route("/upload/newfile", methods=["PUT"])
def upload_to_server():
    if not request.form.get("password") == EV().VIC_user:
        return {"response": "bad password"}, 401
    try:
        # encrypt file on server
        file = request.files['file']
        filename = file.filename
        upload_path = Path(f"app/uploads/{filename}")
        upload_path.parent.mkdir(parents=True, exist_ok=True)
        file.save(upload_path)

        timestamp = datetime.now().strftime("%b %d, %I:%M%p")
        SQL().write_uploads(filename=filename, timestamp=timestamp)

        send_mail_on_new_file_upload(filename=filename)

        return {'response': "OK"}, 200
    except Exception as e: 
        print(e)
        return {"response": "problem on server..."}, 500

@app.route("/upload/fetchfile/<filename>", methods=["GET"])
@require_auth
def fetch_file(filename):
    try:
        path_to_file: Path = Path(f"uploads/{filename}")
        return send_file(path_or_file=path_to_file)
    except Exception as e: 
        print(e)
        return {'resposne': "whoops"}, 500

@app.route("/upload/deletefile", methods=["DELETE"])
@require_auth
def delete_file():
    file:dict = request.get_json()
    file = file.get("filename")
    Path(f"app/uploads/{file}").unlink()
    SQL().delete_uploads(filename=file)
    return {"response": "OK"}, 200

@app.route("/upload/checkpassword", methods=["POST"])
def check_password():
    password:dict = request.get_json()
    password = password.get("password")
    if password == EV().VIC_user:
        return {"response": "OK"}, 200
    return {"response": "bad password"}, 401

@app.route("/upload/checkduplicate", methods=["POST"])
def check_duplicate():
    filename: dict = request.get_json()
    filename = filename.get("filename")
    existing_files: list[dict] = SQL().read_uploads()
    for file in existing_files:
        if file.get("filename") == filename:
            return {"response": "We already have a file with an identical name! "
            f"It looks like you have already uploaded this file: {filename}. "
            "Please check your filename and try again."}, 400
    return {"response": "OK"}, 200