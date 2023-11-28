import os

from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

import requests

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
jwt = JWTManager(app)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    r = requests.post(os.environ["ACCOUNT_SERVICE_URL"]+"/login",json=dict(email=email, password=password))
    if r.status_code == 200:
        access_token = create_access_token(email, additional_claims=r.json())
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Bad email or password"}), 401

    

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/validate", methods=["GET"])
@jwt_required()
def protected():
    # Get current jwt claims
    return jsonify(get_jwt()), 200

if __name__ == "__main__":
    app.run(port=5001)