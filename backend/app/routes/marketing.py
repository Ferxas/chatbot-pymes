from flask_restful import Resource, reqparse
import openai
import os


class MarketingResource(Resource):
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("business_data", type=dict, location="json",
                                 required=True, help="Business data is required")
        self.parser.add_argument(
            "goal", type=str, location="json", required=True, help="Goal is required")

    def post(self):

        args = self.parser.parse_args()
        business_data = args["business_data"]
        goal = args["goal"]

        # basic example or funcitonality
        try:
            response = self.generate_marketing_strategy(business_data, goal)
            return {"strategies": response}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def generate_marketing_strategy(self, business_data, goal):
        
        prompt = (
            f"Eres un asistente experto en marketing para PYMEs. Basándote en la información de contexto proporcionada, ofrece estrategias efectivas, análisis de mercado y recomendaciones personalizadas que permitan a las pequeñas y medianas empresas mejorar su visibilidad, atraer y retener clientes, optimizar sus campañas publicitarias y aprovechar herramientas digitales, como el análisis de datos y la inteligencia artificial, para lograr un crecimiento sostenible en un entorno competitivo."
        )
        
        response = openai.completions.create(
            prompt=prompt,
            temperature=0.9,
            max_tokens=100,
            model="gpt-3.5-turbo-instruct"
        )
        
        return response.choices[0].text.strip() 
