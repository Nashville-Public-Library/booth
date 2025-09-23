import sqlite3

class SQL:
    def __init__(self):
        self.connection = sqlite3.connect("banner.db")
        self.connection.row_factory = sqlite3.Row
        self.create_message_table_if_not_exists()
        self.create_color_table_if_not_exists()
        self.create_heartbeat_table_if_not_exists()
        self.create_uploads_table_if_not_exists()

    def __del__(self):
        self.connection.close()

    def create_message_table_if_not_exists(self):
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS message (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        message TEXT DEFAULT NULL
                        )''')
        self.connection.cursor().execute('''INSERT OR IGNORE INTO message (message) VALUES ('')''')
        self.connection.commit()

    def create_color_table_if_not_exists(self):
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS color (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        color TEXT UNIQUE
                        )''')
        self.connection.cursor().execute('''INSERT OR IGNORE INTO color (color) VALUES ('#a52a2a')''')
        self.connection.commit()

    def create_heartbeat_table_if_not_exists(self):
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS heartbeat (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hostname TEXT UNIQUE,
                        ip_address TEXT,
                        last_seen TEXT
                        )''')
        
    def create_uploads_table_if_not_exists(self):
        self.connection.cursor().execute('''CREATE TABLE IF NOT EXISTS uploads (
                                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                                         filename TEXT,
                                         url TEXT,
                                         token TEXT,
                                         timestamp TEXT
                                         )''')

    def write_message(self, message):
        self.connection.execute('DELETE FROM message')
        self.connection.execute("""INSERT INTO message (message) VALUES(?)""", (message,))
        self.connection.commit()
    
    def read_message(self):
        message = self.connection.execute("""SELECT * FROM message""")
        message = message.fetchone()
        message = message[1]
        return message

    def write_color(self, color):
        self.connection.execute('DELETE FROM color')
        self.connection.execute("""INSERT INTO color (color) VALUES(?)""", (color,))
        self.connection.commit()

    def read_color(self):
        color = self.connection.execute("""SELECT * from color""")
        color = color.fetchone()
        color = color[1]
        return color
    
    def write_heartbeat(self, hostname: str, ip_address: str, last_seen: str):
        self.connection.execute("""
            INSERT INTO heartbeat (hostname, ip_address, last_seen)
            VALUES (?, ?, ?)
            ON CONFLICT(hostname) DO UPDATE SET
                ip_address = excluded.ip_address,
                last_seen = excluded.last_seen
        """, (hostname, ip_address, last_seen))
        self.connection.commit()

    
    def read_heartbeat(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM heartbeat")
        devices = cursor.fetchall()
        ret_val = []
        for device in devices:
            ret_val.append(dict(device))
        return ret_val
    
    def write_uploads(self, filename: str, url: str, token: str, timestamp:str):
        self.connection.execute('''
            INSERT INTO uploads (filename, url, token, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (filename, url, token, timestamp))
        self.connection.commit()

    def read_uploads(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM uploads")
        uploads = cursor.fetchall()
        ret_val = []
        for upload in uploads:
            ret_val.append(dict(upload))
        return ret_val
    
    def delete_uploads(self, filename:str):
        self.connection.execute("DELETE FROM uploads WHERE filename = ?", (filename,))
        self.connection.commit()    