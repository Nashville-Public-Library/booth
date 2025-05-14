from flask import render_template, request, send_from_directory

from app import app

@app.route('/pwa', methods=['GET'])
def pwa():
    return render_template("pwa/index.html")