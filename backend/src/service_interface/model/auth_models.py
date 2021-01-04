from flask_restplus import fields, Model

login_request_model = Model("Login request model", {
    "username": fields.String(pattern="[a-zA-Z0-9]"),
    "password": fields.String(pattern="[a-zA-Z0-9!@#$%^&*()]"),
})


user_model = Model("User model", {
    "id": fields.Integer(),
    "username": fields.String(),
    "email": fields.String(),
})
