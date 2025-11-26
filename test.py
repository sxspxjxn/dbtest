import os, psycopg2
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv('db_url')
if not db_url:
    print("no db_url in .env")
else:
    if 'sslmode' not in db_url:
        sep = '&' if '?' in db_url else '?'
        db_url = db_url + sep + 'sslmode=require'
    try:
        print("Attempting to connect...")
        conn = psycopg2.connect(dsn=db_url, connect_timeout=10)
        print("Connected OK")
        conn.close()
    except Exception as e:
        print("Connection failed:", e)