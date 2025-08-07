from src.app import ma
from src.database.schemas.role import RoleSchema
from marshmallow import fields


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    role = fields.Nested(RoleSchema)


class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)
