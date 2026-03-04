from fabric import Connection, Result
from flask import render_template

from app import app

@app.route("/assets")
def assets():
    connection: Connection = Connection(host="assets")
    result: Result = connection.run("cd shows && ls", hide=True)
    result_stdout:str = result.stdout
    folders = result_stdout.rsplit("\n")
    ret_val: list = []
    for folder in folders:
        if folder != "":
            ret_val.append(folder.lower())
    return render_template("assets_overview.html", folders=ret_val)

@app.route("/assets/folder/<folder>")
def assets_folder(folder):  
    connection: Connection = Connection(host="assets")
    ret_val: list = []
    result: Result = connection.run(f"cd shows/{folder} && ls", hide=True)
    result_stdout:str = result.stdout
    files: list[str] = result_stdout.rsplit("\n")
    for file in files:
        if file != "": # exclude files without names?
            ret_val.append(file.lower())
    return render_template("assets_folder.html", files=ret_val)