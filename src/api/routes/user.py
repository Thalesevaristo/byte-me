from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect

from http import HTTPStatus

from src.utils.utils import requires_roles

from src.database.schemas.user import CreateUserSchema, UserSchema
from src.database.models import User, db
from src.app import bcrypt

from marshmallow import ValidationError


app = Blueprint("user", __name__, url_prefix="/users")


def create_user(data: dict) -> tuple[dict, int]:
    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()

    return {"msg": "User created!"}, HTTPStatus.CREATED


@jwt_required()
@requires_roles("admin")
def list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    users_schema = UserSchema(many=True)
    return users_schema.dump(users)


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
