from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from src.app import User, db
from http import HTTPStatus
from sqlalchemy import inspect

app = Blueprint("auth", __name__, url_prefix="/auth")

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "tes""t" or password != "test":
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    acess_token = create_access_token(identity=username)
    return {"acess_token": acess_token}
