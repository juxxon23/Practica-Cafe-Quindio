from marshmallow import validate, Schema, fields


class ProductRegister(Schema):
    role_a = fields.Str(required=True, validate=validate.Length(min=1, max=2))
    name_a = fields.Str(required=True, validate=validate.Length(min=3, max=40))
    bio_a = fields.Str(validate=validate.Length(min=3, max=200))
    price = fields.Float(required=True)
    id_p = fields.String(required=True, validate=validate.Length(min=1, max=2))

class ProductUpdate(Schema):
    role_a = fields.Str(validate=validate.Length(min=1, max=2))
    name_a = fields.Str(validate=validate.Length(min=3, max=40))
    bio_a = fields.Str(validate=validate.Length(min=3, max=200))
    price = fields.Float()
    id_p = fields.String(validate=validate.Length(min=1, max=2))