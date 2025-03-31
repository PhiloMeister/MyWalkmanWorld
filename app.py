from flask import Flask, request, render_template, redirect, jsonify
import sqlite3
import subprocess
import os
import random
import re

app = Flask(__name__)

# ⚠️ Hardcoded values
SECRET_KEY = "please_dont_hack_me"
DATABASE_PATH = "walkman.sqlite"

# ⚠️ Dummy vulnerabilities hidden in unused functions

def sonar_dummy_flaws():
    # Wrong method arg name
    class Misnamed:
        def log(this):  # should be 'self'
            print("Logging")

    # Public S3 ACL
    s3_acl = {
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:*",
        "Resource": "arn:aws:s3:::walkman-world/*"
    }

    # IAM privilege escalation
    aws_iam_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["iam:PassRole"],
                "Resource": "*"
            }
        ]
    }

    # Regex where str.replace would do
    re.sub(r"walkman", "tape", "walkman model")

    # Assertion comparing incompatible types
    if False:
        assert "model" == 2025

    # Assertion at end of exception block
    try:
        raise ValueError("example")
    except ValueError:
        pass
    if False:
        assert True

    # Bare raise in finally
    try:
        raise Exception("just testing")
    finally:
        if False:
            raise

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

# ⚠️ Vulnerable to SQL Injection
def get_walkmans(search_query=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    if search_query:
        query = f"SELECT * FROM walkmans WHERE model LIKE '%{search_query}%'"
        cursor.execute(query)
    else:
        cursor.execute("SELECT * FROM walkmans")
    results = cursor.fetchall()
    conn.close()
    return results

# ⚠️ Adds a walkman to the DB (no sanitization)
def add_walkman(model, year, description):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
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
        "This one is as good as you"
    ]
    result = random.choice(verdicts)
    return f"<h1>{model}</h1><p>{result}</p>"

@app.route("/run", methods=["POST"])
def run():
    cmd = request.form.get("cmd")
    output = subprocess.check_output(cmd, shell=True)
    return f"<pre>{output.decode()}</pre>"

@app.route("/goto")
def goto():
    target = request.args.get("url", "/")
    return redirect(target)

@app.route("/env")
def env():
    return jsonify(dict(os.environ))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
