import sqlite3

class SQL:
    def __init__(self):
        self.connection = sqlite3.connect("banner.db")
        self.create_message_table_if_not_exists()
        self.create_color_table_if_not_exists()

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