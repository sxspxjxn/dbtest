from flask import Flask, request, session, g, redirect, render_template, url_for, flash
from db import *
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from functools import wraps
import os
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('key', 'fallback')

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if logged_in():
            return function(*args, **kwargs)
        return redirect(url_for('login_page'))
    return wrapper

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if logged_in():
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        success = login(username, password)
        if success:
            session['id'] = success
            return redirect(url_for('index'))
        flash('login unsuccessful', 'error')
        return render_template('login.html')

@app.route('/account', methods=['GET', 'POST'])
def create_account_page():
    if logged_in():
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        success = create_user(username, password)
        if success:
            session['id'] = success
            return redirect(url_for('index'))
        flash('unsuccessful account creation', 'error')
        return render_template('create.html')
@app.route('/testing')
def test():
    try:
        with db_connection() as conn:
            with conn.cursor() as c:
                c.execute('SELECT now()')
                row = c.fetchone()
        return f'db ok: {row}', 200
    except Exception as e:
        print('testing route db error:', e)
        return 'db error', 500
@app.teardown_appcontext
def teardown():
    if hasattr(g, 'db'):
        g.db.close()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
