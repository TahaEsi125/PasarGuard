import sqlite3
from pathlib import Path
from config import DB_PATH

Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

def conn():
    c=sqlite3.connect(DB_PATH)
    c.row_factory=sqlite3.Row
    return c

def init_db():
    with conn() as c:
        c.execute('''CREATE TABLE IF NOT EXISTS customers (telegram_id INTEGER PRIMARY KEY, username TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER, panel_username TEXT, plan TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')

def save_customer(tid, username):
    with conn() as c: c.execute('INSERT OR REPLACE INTO customers(telegram_id,username) VALUES(?,?)',(tid,username))

def save_order(tid, panel_username, plan):
    with conn() as c: c.execute('INSERT INTO orders(telegram_id,panel_username,plan) VALUES(?,?,?)',(tid,panel_username,plan))

def orders_count():
    with conn() as c: return c.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
