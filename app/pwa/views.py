from flask import render_template, request, send_from_directory

from app import app

@app.route('/pwa', methods=['GET'])
def pwa():
    return app.send_static_file("pwa/pages/index.html")

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')
