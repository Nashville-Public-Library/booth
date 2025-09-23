from flask import render_template, request
import waifuvault
import io

from app import app

@app.route("/upload", methods=['GET'])
def upload():
    return render_template("upload.html")

@app.route("/upload/file", methods=["POST"])
def upload_to_server():
    json: dict = request.get_json() 
    print(json)

    return {'response': "OK"}, 200