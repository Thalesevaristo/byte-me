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
    _query = db.select(User).where(User.username == username)
    user = db.session.execute(_query).scalar()
    if not user or user.password != password:
        return {"message": "Wrong name or password. Try again."}

    if username != "tes""t" or password != "test":
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    acess_token = create_access_token(identity=user.id)
    return {"acess_token": acess_token}
