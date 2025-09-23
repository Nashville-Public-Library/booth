from flask import render_template, request
import waifuvault
import io

from app import app
from app.sql import SQL

@app.route("/upload", methods=['GET'])
def upload():
    return render_template("upload.html")

@app.route("/upload/file", methods=["POST"])
def upload_to_server():
    json: dict = request.get_json() 
    sql = SQL()
    sql.write_uploads(filename=json.get("filename"), url=json.get("url"), token=json.get("token"))

    return {'response': "OK"}, 200

@app.route("/upload/uploads")
def uploads():
    sql = SQL()
    print(sql.read_uploads())
    return "OK"