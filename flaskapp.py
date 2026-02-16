import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'users.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database Setup
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT, password TEXT, firstname TEXT, lastname TEXT, 
                  email TEXT, address TEXT, word_count INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def landing():
    # New Landing Page
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Removed File Upload from here
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        address = request.form['address']
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (username, password, firstname, lastname, email, address, 0)) # Default word_count to 0
        conn.commit()
        conn.close()

        # Redirect to login after registration
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            return redirect(url_for('profile', username=username))
        return render_template('login.html', error="ACCESS DENIED")
    
    return render_template('login.html')

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return render_template('profile.html', user=user)

# New Route specifically for File Upload
@app.route('/upload/<username>', methods=['POST'])
def upload_file(username):
    file = request.files['file']
    if file and file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, 'Limerick.txt')
        file.save(file_path)
        
        # Calculate word count
        content = open(file_path, 'r').read()
        word_count = len(content.split())
        
        # Update DB
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("UPDATE users SET word_count=? WHERE username=?", (word_count, username))
        conn.commit()
        conn.close()
        
    return redirect(url_for('profile', username=username))

@app.route('/download')
def download():
    return send_from_directory(UPLOAD_FOLDER, 'Limerick.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
