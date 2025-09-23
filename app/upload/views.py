from datetime import datetime

from flask import render_template, request
import waifuvault
import io

from app import app
from app.sql import SQL

@app.route("/upload", methods=['GET'])
def upload():
    return render_template("upload.html")

@app.route("/upload/viewfiles", methods=["GET"])
def view_files():
    sql = SQL()
    files = sql.read_uploads()
    return render_template("view_upload_files.html", files=files)

@app.route("/upload/newfile", methods=["POST"])
def upload_to_server():
    json: dict = request.get_json() 
    timestamp = datetime.now().strftime("%b %d, %I:%M%p")
    sql = SQL()
    sql.write_uploads(filename=json.get("filename"), url=json.get("url"), token=json.get("token"), timestamp=timestamp)

    return {'response': "OK"}, 200

@app.route("/upload/deletefile", methods=["DELETE"])
def delete_file():
    file:dict = request.get_json()
    file = file.get("filename")
    sql = SQL()
    sql.delete_uploads(filename=file)
    return {"response": "OK"}, 200

@app.route("/upload/uploads", methods=["POST"])
def uploads():
    sql = SQL()
    files = sql.read_uploads()
    return {"files": files}