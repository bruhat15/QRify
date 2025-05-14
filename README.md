# QRify – QR Code Generator

A lightweight Flask web application that lets users register, log in, and instantly generate QR codes for URLs, free-form text, or contact information. Generated codes are previewed in the browser and downloadable as PNG files, with a simple history feature backed by SQLite.

---

## 🚀 Features

- **User authentication**  
  Sign up, log in/out, and session management via secure password hashing (Werkzeug).
- **Instant QR generation**  
  Create QR codes on demand using the `qrcode` library (configurable error-correction, box size, border).
- **Inline preview & download**  
  Stream images in memory (`io.BytesIO`), encode in Base64 for preview, and serve one-click PNG downloads via Flask’s `send_file`.
- **History tracking**  
  Persist each generation event (payload type, content, timestamp) in SQLite so users can revisit recent codes.
- **Minimal dependencies**  
  Pure-Python stack—no Docker required, no heavy JS frameworks.

---

## 🏠 Implementation

```
QRify-main/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html          # Base layout
│   ├── index.html         # QR input & preview page
│   ├── login.html         # Login form
│   └── signup.html        # Signup form
└── static/
    └── css/               # (optional) custom styles
```

- **`app.py`**
  - Defines routes:
    - `/` (GET/POST) – form to enter payload, generate and preview QR  
    - `/download_qr` (GET) – serves the last QR image as a downloadable PNG  
    - `/signup`, `/login`, `/logout` – user account flows  
  - Uses:
    - **Flask** for routing, sessions, and `send_file`  
    - **qrcode** (uses Pillow) for image creation  
    - **io.BytesIO** + **base64** for in-memory image handling  
    - **sqlite3** for storing users and history  
    - **werkzeug.security** for password hashing

- **Templates** (`templates/`)  
  - A simple Jinja2 layout with a form, preview `<img>` tag bound to Base64 data, and history list

---

## ⚙️ How It Works (User Flow)

1. **Sign up & log in**  
   User creates an account (username/password) and is assigned a session cookie
2. **Generate a QR code**  
   On the home page, user selects a type (URL, text, contact) and enters the content
3. **Server-side creation**  
   - `qrcode.QRCode(...)` builds the QR matrix  
   - A PIL image is generated, written to `io.BytesIO`, then encoded to Base64 for inline `<img>` display  
   - The same buffer is kept in session memory so `/download_qr` can stream it back as a PNG
4. **History**  
   Each generation is logged (type, raw payload, timestamp) in SQLite. The home page shows the last 5 entries
5. **Download**  
   Clicking “Download” triggers `/download_qr`, which reads the buffer, sets headers, and returns a PNG attachment

---

## 💻 Installation & Running

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/QRify-main.git
   cd QRify-main
   ```

2. **Create & activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   .venv\Scripts\activate.bat     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure**
   - In `app.py`, set `app.secret_key = "<your-secret-key>"` or export it as an env var:  
     ```bash
     export FLASK_SECRET_KEY="a_very_secret_key"
     ```
   - By default, SQLite database (`users.db`) will be created automatically on first run.

5. **Run the server**
   ```bash
   flask run
   ```
   Or directly:
   ```bash
   python app.py
   ```

6. **Open in browser**  
   Visit http://127.0.0.1:5000 to sign up, log in, and start generating QR codes

---

## 📋 Requirements

- Python 3.7+
- Flask
- qrcode
- Pillow (installed as a dependency of qrcode)
- sqlite3 (built-in)

---

## 🔑 Key Learnings

- Building simple authenticated workflows in Flask  
- Handling in-memory binary streams and Base64 encoding  
- Lightweight persistence with SQLite and Python’s standard library  
- Exposing dynamic image content for inline preview and file download

---

Feel free to adapt, extend, or file issues/PRs. Enjoy QRify! 🚀
