from flask import render_template, request, send_from_directory

from app import app

@app.route('/pwa', methods=['GET'])
def pwa():
    return app.send_static_file("pwa/pages/index.html")

# @app.route('/pwa/sw.js')
# def service_worker():
#     return app.send_static_file('pwa/sw.js')