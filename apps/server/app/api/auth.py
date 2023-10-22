from app.api import api
from flask_restx import Resource

auth_ns = api.namespace("auth", description="Operations for authentication")


class Test(Resource):
    def get(self):
        return {"m":"p"}