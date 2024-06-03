from flask import Flask, render_template, request, send_file, redirect, url_for, session
import qrcode,os
from io import BytesIO
import base64
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
def init_db():
    if not os.path.exists('users.db'):
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT UNIQUE NOT NULL,
                              password TEXT NOT NULL)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              user_id INTEGER,
                              data TEXT,
                              date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              FOREIGN KEY (user_id) REFERENCES users (id))''')
        conn.commit()

# Initialize database
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    qr_code_base64 = None
    if request.method == "POST":
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            user_id = None
        
        data = request.form.to_dict()
        qr_type = data.pop('type')
        content = ""

        if qr_type == "link":
            content = data.get("link")
        elif qr_type == "email":
            content = f"mailto:{data.get('email')}"
        elif qr_type == "text":
            content = data.get("text")
        elif qr_type == "call":
            content = f"tel:{data.get('phone')}"
        elif qr_type == "sms":
            content = f"smsto:{data.get('phone')}"
        elif qr_type == "vcard":
            content = f"BEGIN:VCARD\nFN:{data.get('name')}\nTEL:{data.get('phone')}\nEMAIL:{data.get('email')}\nEND:VCARD"
        elif qr_type == "wifi":
            content = f"WIFI:T:{data.get('auth')};S:{data.get('ssid')};P:{data.get('password')};"

        if content:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,  # Adjust box size here
                border=4,
            )
            qr.add_data(content)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            if user_id:
                with sqlite3.connect('users.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO history (user_id, data) VALUES (?, ?)''', (user_id, content))
                conn.commit()

            # Save QR code data in session
            session['qr_code_base64'] = qr_code_base64

    return render_template("index.html", qr_code_base64=qr_code_base64)

@app.route("/download_qr", methods=["GET"])
def download_qr():
    if 'qr_code_base64' in session:
        qr_code_base64 = session['qr_code_base64']
        buffer = BytesIO(base64.b64decode(qr_code_base64))
        session.pop('qr_code_base64')  # Clear session data after download
        return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='qr_code.png')
    return redirect(url_for('index'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, hashed_password))
                conn.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return "Username already exists!"
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                return redirect(url_for('index'))
            else:
                return "Invalid username or password!"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)