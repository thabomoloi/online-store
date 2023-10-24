from flask_restx import Model, fields

base_model = Model("BaseModel",{
    "code": fields.Integer,
    "description": fields.String
})

error_model = base_model.clone("Error", {
    "message": fields.String,
})

error_400 = error_model.clone("Error",{
    "code": fields.Integer(example=400),
    "description": fields.String(example="Bad Request"),
    "message": fields.String(example="The request was invalid.")
})
