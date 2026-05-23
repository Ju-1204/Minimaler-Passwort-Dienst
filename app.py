from flask import Flask, jsonify
import secrets
import string

app = Flask(__name__)

def generate_password(length=10):
    alphabet = string.ascii_letters + string.digits + "!§$%&/?#"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@app.route("/generate_pw", methods=["GET"])
def generate_pw():
    password = generate_password()

    return jsonify({
        "generated_password": password
    })

if __name__ == "__main__":
    app.run(debug=True)