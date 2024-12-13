from flask_restful import Resource, reqparse

class PredictionsResource(Resource):
    def __init__(self):
        
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("data", type=list, location="json", required=True, help="Data is required and must be a list")
        self.parser.add_argument("model", type=str, location="json", required=True, help="Model name is required")
        
    def post(self):
        # basic example
        
        args = self.parser.parse_args()
        data = args["data"]
        model_name = args["model"]        
        
        try:
            predictions = self.predict(data, model_name)
            return {"prediction": predictions}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    def predict(self, data, model_name):
        # example data, for now
        
        return [f"Prediction for {item} using model {model_name}" for item in data]