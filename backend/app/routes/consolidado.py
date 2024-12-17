from flask_restful import Resource, reqparse
import openai
import os
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class FODAResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("business_data", type=dict, location="json", required=True,
                                 help="Business data is required")

        # Validar clave API de OpenAI
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("La clave de API de OpenAI no está configurada. Configura la variable 'OPENAI_API_KEY'.")
        openai.api_key = self.openai_api_key

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
            "Eres un asistente experto en consultoría empresarial para PYMEs. Basándote en la información de contexto "
            "proporcionada, proporciona soluciones estratégicas, análisis financieros, y recomendaciones prácticas que "
            "permitan a las pequeñas y medianas empresas mejorar su eficiencia operativa, optimizar sus recursos, "
            "adaptarse a cambios del mercado y alcanzar sus objetivos de crecimiento sostenible.\n\n"
            f"Datos del negocio: {business_data}\n\n"
            "Por favor, proporciona el análisis en formato estructurado con cada sección claramente identificada."
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Modelo correcto para completions basadas en chat
            messages=[
                {"role": "system", "content": "Eres un asistente experto en consultoría empresarial para PYMEs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
            top_p=1,
        )

        # Validación de respuesta
        if "choices" not in response or len(response.choices) == 0:
            raise ValueError("La respuesta de OpenAI está vacía o no contiene datos válidos.")
        return response.choices[0].message.content.strip()


# Consolidado del archivo JSON (QA.json)
def consolidate_files():
    archivos = [
        "foda.py",
        "marketing.py",
        "predictions.py",
        "QA.json"
    ]

    # Rutas basadas en el directorio actual
    base_dir = os.path.abspath(os.path.dirname(__file__))
    salida_path = os.path.join(base_dir, "consolidado.py")

    with open(salida_path, "w", encoding="utf-8") as salida:
        salida.write("# Archivo Consolidado\n\n")
        for archivo in archivos[:-1]:
            file_path = os.path.join(base_dir, archivo)
            with open(file_path, "r", encoding="utf-8") as f:
                salida.write(f"# Contenido de {archivo}\n")
                salida.write(f.read())
                salida.write("\n\n")

        # Consolidación del JSON como variable
        qa_path = os.path.join(base_dir, "QA.json")
        with open(qa_path, "r", encoding="utf-8") as f:
            qa_data = json.load(f)
            salida.write("# Contenido de QA.json\n")
            salida.write("qa_data = ")
            json.dump(qa_data, salida, indent=4, ensure_ascii=False)

    print(f"Archivo consolidado creado: {salida_path}")


if __name__ == "__main__":
    consolidate_files()
