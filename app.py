
from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "/app/data/app.db")

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mahasiswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL
            )
        """)

@app.route('/')
def hello():
    return "Halo dari Flask + Docker + Jenkins + SQLite!"

@app.route('/mahasiswa', methods=['GET'])
def get_mahasiswa():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM mahasiswa").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route('/mahasiswa', methods=['POST'])
def add_mahasiswa():
    data = request.get_json(silent=True) or {}
    nama = data.get('nama')

    if not isinstance(nama, str) or not nama.strip():
        return jsonify({"error": "Nama wajib diisi"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO mahasiswa (nama) VALUES (?)",
            (nama.strip(),)
        )
        mahasiswa_id = cursor.lastrowid

    return jsonify({
        "id": mahasiswa_id,
        "nama": nama.strip()
    }), 201

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    return "Webhook received", 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)
