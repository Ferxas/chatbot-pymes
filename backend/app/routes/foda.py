from flask_restful import Resource

class FODAResource(Resource):
    def get(self):
        return {"message": "FODA analysis endpoint working!"}, 200