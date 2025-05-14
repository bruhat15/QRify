```markdown
# QRify – QR Code Generator

A lightweight Flask application that lets users generate, preview, download, and track custom QR codes for URLs, free‑form text, or contact details.

---

## 📖 Overview

QRify turns any piece of data—links, messages, email addresses, phone numbers, vCard contacts, Wi‑Fi credentials—into a polished QR code PNG in seconds. It also stores a simple history so you can revisit your last few creations without re‑typing.

![QRify Demo](./assets/qrify_screenshot.png)

---

## ⚙️ How It Works

1. **User interacts**  
   - Visits `/` (index), selects a payload type (URL, text, contact, etc.), and submits the data.
2. **QR generation**  
   - The server receives form data in a Flask route.
   - It instantiates `qrcode.QRCode` with your preferred error‑correction, box‑size, and border.
   - Builds the `PIL.Image` object and writes it into an in‑memory buffer (`io.BytesIO`).
3. **Preview & download**  
   - The PNG is Base64‑encoded and rendered inline on the page for instant preview.
   - A “Download” button triggers a Flask `send_file` response, streaming the raw PNG back to the browser.
4. **History logging**  
   - If you’re signed in, each generation event (type, payload, timestamp) is appended to an SQLite table.
   - The index page shows your five most recent codes, so you can quickly regenerate or download past entries.
5. **Authentication**  
   - Simple signup/login/logout functionality with password hashing (`werkzeug.security`).
   - Uses Flask sessions to gate history access and enforce per‑user tracking.

---

## 🏗️ Project Structure

```

QRify/
├── app.py                  # Main Flask application and route definitions
├── templates/              # Jinja2 HTML templates (index, login, signup)
├── static/                 # CSS, JS, images (optional)
├── assets/                 # Project images (e.g., README screenshot)
├── requirements.txt        # Python dependencies
└── users.db                # SQLite database file (auto‑created)

````

---

## 🚀 Quick Start

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/QRify.git
   cd QRify
````

2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   The first time you run, `app.py` will automatically create `users.db` with `users` and `history` tables. No manual SQL needed.

5. **Run the app**

   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development   # optional: enables debug mode
   flask run
   ```

   By default, your service is available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

6. **Use QRify**

   * Open the browser to the root URL.
   * Sign up or log in to track your history.
   * Enter data, click **Generate**, preview your QR code, then click **Download**.

---

## 📦 Dependencies

Listed in `requirements.txt`:

* **Flask** — Web framework
* **qrcode** — QR image generation (depends on Pillow)
* **Pillow** — Underlying image library (installed by `qrcode`)
* **werkzeug** — Security utilities for password hashing
* **itsdangerous**, **Jinja2**, **click** — Flask’s core deps (auto‑installed)

---

## 🔑 Key Learnings

* Building dynamic image‑generation endpoints in Flask
* Handling in‑memory binary streams with `io.BytesIO`
* Base64 encoding for fast inline previews
* Lightweight persistence with SQLite and Python’s `sqlite3`
* Session‑based authentication and secure password hashing

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add YourFeature"`)
4. Push to your fork (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📄 License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

```

Feel free to adjust any paths, screenshot links, or commands to match your setup and preferred conventions.
```
