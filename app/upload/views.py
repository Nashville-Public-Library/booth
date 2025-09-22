from flask import render_template, request
import waifuvault
import io

from app import app

@app.route("/upload", methods=['GET'])
def upload():
    return render_template("upload.html")

@app.route("/upload/file", methods=["POST"])
def upload_to_server():
    file = request.files["file"]

    file_like = io.BytesIO(file.read())

    upload_file = waifuvault.FileUpload(target=file_like, target_name=file.filename, expires="20d")
    upload_res = waifuvault.upload_file(upload_file)
    print(f"{upload_res.url}")
    

    return {'response': "OK"}, 200