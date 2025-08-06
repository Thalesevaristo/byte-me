from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect

from src.models import User, db
from src.utils import requires_roles
from src.app import bcrypt

from http import HTTPStatus

app = Blueprint("user", __name__, url_prefix="/users")


def create_user(data: dict) -> tuple[dict, int]:
    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()

    return {"msg": "User created!"}, HTTPStatus.CREATED


def list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
            },
        }
        for user in users
    ]


def get_user(user: User) -> dict:

    return {"id": user.id, "username": user.username}


def update_user(user: User, data: dict) -> tuple[dict, int]:
    mapper = inspect(User)
    for column in mapper.attrs:
        key = column.key
        if key in data:
            setattr(user, key, data[key])
    db.session.commit()

    return get_user(user), HTTPStatus.OK


def delete_user(user: User) -> tuple[str, int]:
    db.session.delete(user)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT


@app.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_roles("admin")
def handle_user():

    if request.method == "POST":
        data = request.get_json()
        return create_user(data)

    else:
        return {"users": list_users()}, HTTPStatus.OK


@app.route("/<int:user_id>", methods=["GET", "PATCH", "DELETE"])
@jwt_required()
def user_control(user_id: int):
    user = db.get_or_404(User, user_id)

    if request.method == "PATCH":
        data = request.get_json()
        return update_user(user, data)

    elif request.method == "DELETE":
        return delete_user(user)

    else:
        return get_user(user), HTTPStatus.OK
