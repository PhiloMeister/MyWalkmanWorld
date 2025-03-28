from flask import Flask, request, render_template, redirect, jsonify
import sqlite3
import subprocess
import os
import random

app = Flask(__name__)

# 🚨 Hardcoded values
SECRET_KEY = "please_dont_hack_me"
DATABASE_PATH = "walkman.sqlite"

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS walkmans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL UNIQUE,
            year INTEGER NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()


# 🚨 Vulnerable to SQL Injection
def get_walkmans(search_query=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    if search_query:
        query = f"SELECT * FROM walkmans WHERE model LIKE '%{search_query}%'"
        cursor.execute(query)  # 🚨 Injection risk
    else:
        cursor.execute("SELECT * FROM walkmans")
    results = cursor.fetchall()
    conn.close()
    return results

# 🚨 Adds a walkman to the DB (no sanitization)
def add_walkman(model, year, description):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    # 🚨 SQL Injection vulnerability (intentionally insecure)
    query = f"INSERT INTO walkmans (model, year, description) VALUES ('{model}', {year}, '{description}')"
    cursor.execute(query)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        model = request.form.get("model", "")
        year = request.form.get("year", "")
        description = request.form.get("description", "")
        if model and year and description:
            try:
                add_walkman(model, year, description)
                message = f"✅ Added: {model}"
            except Exception as e:
                message = f"❌ Error adding: {e}"
        else:
            message = "❌ All fields are required."
    search_query = request.args.get("search", "")
    walkmans = get_walkmans(search_query)
    return render_template("index.html", walkmans=walkmans, search_query=search_query, message=message)

@app.route("/rate", methods=["GET"])
def rate():
    model = request.args.get("model", "")
    verdicts = [
        "This one is good.",
        "This one is not good.",
        "This one is shit 100%."
    ]
    result = random.choice(verdicts)
    return f"<h1>{model}</h1><p>{result}</p>"

# 🚨 RCE
@app.route("/run", methods=["POST"])
def run():
    cmd = request.form.get("cmd")
    output = subprocess.check_output(cmd, shell=True)  # 🚨 Remote Code Execution
    return f"<pre>{output.decode()}</pre>"

# 🚨 Open redirect
@app.route("/goto")
def goto():
    target = request.args.get("url", "/")
    return redirect(target)

# 🚨 Expose environment variables
@app.route("/env")
def env():
    return jsonify(dict(os.environ))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)  # 🚨 Debug mode ON
