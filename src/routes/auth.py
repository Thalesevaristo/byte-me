from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from src.models import db, User
from src.app import bcrypt
from http import HTTPStatus

app = Blueprint("auth", __name__, url_prefix="/auth")


def _check_password(password_hash, raw_password):
    return bcrypt.check_password_hash(
        pw_hash=password_hash,
        password=raw_password,
    )


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", None)
    password = data.get("password", None)

    query = db.select(User).where(User.username == username)
    user = db.session.execute(query).scalar()

    if not user or not _check_password(user.password, password):
        return {
            "msg": "Wrong name or password. Try again.",
        }, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}
