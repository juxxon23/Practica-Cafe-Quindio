from marshmallow import validate, Schema,fields

class ClientSignin(Schema):
    name_c = fields.Str(required=True, validate= validate.Length(min= 3, max=20))
    email = fields.Str(required=True, validate=validate.Length(min=13, max= 130))
    phone = fields.Str(required=True, validate= validate.Length(min=7, max=10))
    password = fields.String(required=True, validate=validate.Length(min=8, max= 20))

class ClientLogin(Schema):
    email = fields.Str(required=True, validate=validate.Length(min=13, max=130))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=20))