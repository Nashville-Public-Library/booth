from pathlib import Path

from fabric import Connection, Result
from flask.wrappers import Request
import requests

class SSH:
    def __init__(self):
        self.connection: Connection =  Connection(host="assets")

    def assets(self):
        return self._get_folders()
    
    def assets_folder_folder(self, folder):
        return self._get_items_in_folder(folder=folder)
    
    def assets_folder_feed(self, request_json: Request):
        json: dict = request_json.json
        folder = json.get("folder")
        url: str = f"https://assets.library.nashville.gov/talkinglibrary/shows/{folder}/feed.xml"
        req = requests.get(url)
        feed = req.text
        return {"feed": feed}        
    
    def assets_folder_feed_edit(self, request_json: Request):
        json: dict = request_json.json
        feed = json.get("feed")
        folder = json.get("folder")
        path = Path(f"tmp/feeds/{folder}/feed.xml")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(feed)
        self._upload_file(folder=folder, file=path)
        path.unlink()
        return {"response": f"The RSS feed for {folder} has been updated"} 

    def assets_folder_upload(self, request_json: Request):
        file = request_json.files["file"]
        file_name = file.filename
        folder = request_json.form.get("folder")
        path = Path(f"tmp/{folder}/{file_name}")
        path.parent.mkdir(parents=True, exist_ok=True)
        file.save(path)
        self._upload_file(folder=folder, file=path)
        path.unlink()
        return {"response": f"{file_name} has been uploaded to {folder}"}, 200

    def _get_folders(self) -> list:
        result: Result = self.connection.run("cd shows && ls", hide=True)
        result_stdout:str = result.stdout
        folders = result_stdout.rsplit("\n")
        ret_val: list = []
        for folder in folders:
            if folder != "":
                ret_val.append(folder.lower())
        return ret_val
    
    def _get_items_in_folder(self, folder:str) -> list:  
        if not self._check_folder_exists(folder=folder):
            raise FileExistsError (f"{folder} does not exist on {self.connection.host}")
        ret_val: list = []
        result: Result = self.connection.run(f"cd shows/{folder} && ls", hide=True)
        result_stdout:str = result.stdout
        files: list[str] = result_stdout.rsplit("\n")
        for file in files:
            if file != "": # exclude files without names?
                ret_val.append(file.lower())
        return ret_val
    
    def _upload_file(self, folder: str, file: Path) -> None:
        self.connection.put(local=file, remote=f"shows/{folder}", preserve_mode=False)

    def _check_folder_exists(self, folder: str) -> bool:
        folders = self._get_folders()
        if folder.lower() in folders:
            return True