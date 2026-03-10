from fabric import Connection, Result

class SSH:
    def __init__(self):
        self.connection: Connection =  Connection(host="assets")

    def get_folders(self):
        result: Result = self.connection.run("cd shows && ls", hide=True)
        result_stdout:str = result.stdout
        folders = result_stdout.rsplit("\n")
        ret_val: list = []
        for folder in folders:
            if folder != "":
                ret_val.append(folder.lower())
        return ret_val
    
    def get_items_in_folder(self, folder:str):
        ret_val: list = []
        result: Result = self.connection.run(f"cd shows/{folder} && ls", hide=True)
        result_stdout:str = result.stdout
        files: list[str] = result_stdout.rsplit("\n")
        for file in files:
            if file != "": # exclude files without names?
                ret_val.append(file.lower())
        return ret_val