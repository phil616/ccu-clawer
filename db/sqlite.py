from sqlite3 import connect, Cursor

from pathlib import Path

class Record:
    def __init__(self, url:str, status:int, hex:str, path:str):
        self.url = url
        self.status = status
        self.hex = hex
        self.path = path


def init_db():
    db_path = Path(__file__).parent / 'ccu-clawer.sqlite'
    conn = connect(db_path)
    with conn:
        cur = conn.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS urls (
                    url varchar(255),
                    status INTEGER, 
                    hex varchar(255) PRIMARY KEY, 
                    path varchar(255)
                    )
                    ''')
        # cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS url_index ON urls (url)''')

def insert(url:str, status:int, hex:str,path:str):
    db_path = Path(__file__).parent / 'ccu-clawer.sqlite'
    conn = connect(db_path)
    with conn:
        cur = conn.cursor()
        cur.execute('''INSERT INTO urls VALUES (?, ?, ?, ?)''', (url, status, hex, path))

def get_all():
    db_path = Path(__file__).parent / 'ccu-clawer.sqlite'
    conn = connect(db_path)
    with conn:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM urls''')
        return [Record(*row) for row in cur]

def filter_hex(hex:str):
    db_path = Path(__file__).parent / 'ccu-clawer.sqlite'
    conn = connect(db_path)
    with conn:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM urls WHERE hex=?''', (hex,))
        return [Record(*row) for row in cur]