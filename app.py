from flask import Flask, request, render_template, jsonify
import sqlite3
import os
import subprocess

app = Flask(__name__)

# 🚨 Hardcoded Secret Key (SAST Issue)
SECRET_KEY = "supersecretkey123"

# 🚨 Hardcoded Database Path (SAST Issue)
DATABASE_URL = "walkman.sqlite"

# 🚨 Hardcoded Admin Credentials (SAST Issue)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# 🚨 Dangerous Database Query with SQL Injection (SAST & DAST Issue)
def get_walkmans(search_query=None):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    if search_query:
        # 🚨 SQL Injection vulnerability (f-string query)
        query = f"SELECT * FROM walkmans WHERE model LIKE '%{search_query}%'"
        cursor.execute(query)  # No input sanitization!
    else:
        cursor.execute("SELECT * FROM walkmans")
    walkmans = cursor.fetchall()
    conn.close()
    return walkmans

# 🚨 Unauthenticated Admin Panel (DAST Issue)
@app.route("/admin")
def admin_panel():
    return "<h1>Admin Panel - No Authentication Required</h1><p>Anyone can access this!</p>"

# 🚨 Open Redirect Vulnerability (DAST Issue)
@app.route("/redirect")
def unsafe_redirect():
    url = request.args.get("url")
    return f'<meta http-equiv="refresh" content="0; URL={url}">', 302

# 🚨 Remote Code Execution (SAST & DAST Issue)
@app.route("/execute", methods=["POST"])
def execute_command():
    command = request.form.get("command")
    result = subprocess.check_output(command, shell=True)  # 🚨 Dangerous!
    return jsonify({"result": result.decode()})

# 🚨 Debug Route Exposing Sensitive Environment Variables (SAST Issue)
@app.route("/debug")
def debug():
    return jsonify(dict(os.environ))  # Exposes all environment variables!

# 🚨 Home Page with Vulnerable Search Field
@app.route("/", methods=["GET"])
def home():
    search_query = request.args.get("search", "")
    walkmans = get_walkmans(search_query)
    return render_template("index.html", walkmans=walkmans, search_query=search_query)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # 🚨 Debug Mode Enabled (Security Risk)
