import os, psycopg2
from psycopg2.extras import RealDictCursor
from flask import session, g
from sec import hashed
def db_connection():
    if not hasattr(g, 'db'):
        db_url = os.getenv('db_url')
        g.db = psycopg2.connect(db_url)
        g.db.autocommit = True
    return g.db
def logged_in():
    id = session_id()
    if not id:
        return False
    if not user_by_id(id):
        return False
    return True

def init_db():
    with db_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users(
                  id SERIAL PRIMARY KEY, 
                  username TEXT UNIQUE NOT NULL, 
                  password TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS messages(
                  id SERIAL PRIMARY KEY,
                  userid INTEGER NOT NULL,
                  message TEXT,
                  timestamp TEXT
                  )''')
        
def id_by_user(user: str):
    with db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username = %s', (user,))
        result = c.fetchone()
        return result
def user_by_id(id: int):
    with db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT username FROM users WHERE id = %s', (id,))
        result = c.fetchone()
        return result
def session_id():
    return session.get('id')
def login(username: str, password: str):
    with db_connection() as conn:
        c = conn.cursor(cursor_factory=RealDictCursor)
        c.execute('SELECT id FROM users WHERE username = %s AND password = %s', (username, hashed(password)))
        result = c.fetchone()
        if result:
            id = result.get('id')
        else:
            id = None
        return id if id else False

def create_user(user: str, password: str):
    try:
        with db_connection() as conn:
            c = conn.cursor()
            if not id_by_user(user):
                c.execute('INSERT INTO users(username, password) VALUES (%s, %s)', (user, hashed(password)))
                return True
            return False
    except Exception as e:
        print(f'error: {e}')
        return False