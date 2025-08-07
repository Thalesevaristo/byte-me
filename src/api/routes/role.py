from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.database.schemas.role import CreateRoleSchema, RoleSchema
from src.database.models import db, Role

from src.utils.utils import requires_roles

from http import HTTPStatus

app = Blueprint("role", __name__, url_prefix="/roles")


@requires_roles("admin")
def create_role(data: dict) -> tuple[dict, int]:
    role_schema = CreateRoleSchema()
    try:
        data = role_schema.load(request.get_json())
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    role = Role(id=data["id"], name=data["name"])
    db.session.add(role)
    db.session.commit()

    return {"msg": "Role created!"}, HTTPStatus.CREATED


def list_roles():
    query = db.select(Role)
    roles = db.session.execute(query).scalars().all()
    roles_schema = RoleSchema(many=True)
    return roles_schema.dump(roles)


@app.route("/", methods=["GET", "POST"])
@jwt_required()
def handle_roles():
    if request.method == "POST":
        data = request.get_json()
        return create_role(data)

    else:
        return {"roles": list_roles()}, HTTPStatus.OK
