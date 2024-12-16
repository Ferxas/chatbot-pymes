from flask_restful import Resource, reqparse
import openai
import os

class FODAResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("business_data", type=dict, location="json", required=True, help="Business data is required")
        
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        
    def post(self):
        args = self.parser.parse_args()
        business_data = args["business_data"]
        
        try:
            foda_analysis = self._generate_foda_analysis(business_data)
            return {"foda_analysis": foda_analysis}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
        
    def _generate_foda_analysis(self, business_data):
        prompt = (
            f"Eres un asistente experto en consultoría empresarial para PYMEs. Basándote en la información de contexto proporcionada, proporciona soluciones estratégicas, análisis financieros, y recomendaciones prácticas que permitan a las pequeñas y medianas empresas mejorar su eficiencia operativa, optimizar sus recursos, adaptarse a cambios del mercado y alcanzar sus objetivos de crecimiento sostenible."
            f"Datos del negocio: {business_data}"
            f"Por favor, proporciona el análisis en formato estructurado con cada sección claramente identificada"  
        )
        
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )
        
        return response.choices[0].text.strip()