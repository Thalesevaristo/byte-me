from src.app import ma
from marshmallow import fields


class RoleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)


class CreateRoleSchema(ma.Schema):
    id = fields.Integer(required=True, strict=True)
    name = fields.String(required=True)
