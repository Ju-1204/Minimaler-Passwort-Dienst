from flask import Flask, jsonify, request
import secrets
import string
import bcrypt
import json
import os

app = Flask(__name__)
STORE_FILE = "pw_speichern.json"

def load_passwords():
    if not os.path.exists(STORE_FILE):
        return {}

    with open(STORE_FILE, "r") as file:
        return json.load(file)

def save_passwords(data):
    with open(STORE_FILE, "w") as file:
        json.dump(data, file, indent=4)

def generate_password(length=10):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@app.route("/add_pw", methods=["POST"])

def add_pw():
    data = request.get_json()

    user_id = data.get("user_id")
    clear_pw = data.get("clear_pw")

    if not user_id:
        return jsonify({"error": "user_id fehlt"}), 400


    hashed_pw = bcrypt.hashpw(
        clear_pw.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    passwords = load_passwords()

    passwords[user_id] = hashed_pw

    save_passwords(passwords)

    return jsonify({
        "message": "Passwort gespeichert"
    })

@app.route("/check_pw", methods=["POST"])
def check_pw():

    data = request.get_json()

    user_id = data.get("user_id")
    clear_pw = data.get("clear_pw")

    passwords = load_passwords()

    if user_id not in passwords:
        return jsonify({
            "valid": False,
            "message": "Benutzer nicht gefunden"
        }), 404

    stored_hash = passwords[user_id].encode("utf-8")

    valid = bcrypt.checkpw(
        clear_pw.encode("utf-8"),
        stored_hash
    )
    return jsonify({
        "valid": valid
    })

@app.route("/generate_pw", methods=["GET"])
def generate_pw():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id fehlt"}), 400

    password = generate_password()

    hashed_pw = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    passwords = load_passwords()
    passwords[user_id] = hashed_pw
    save_passwords(passwords)

    return jsonify({
        "user_id": user_id,
        "generated_password": password
    })

if __name__ == "__main__":
    app.run(debug=True)