from flask_restful import Resource, reqparse
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import os
import openai

class PredictionsResource(Resource):
    def __init__(self):
        # Parser para manejar datos de entrada
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("query", type=str, location="json", required=True, help="Query is required.")

        # Modelo para embeddings (FAISS)
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Configuración de FAISS para búsquedas rápidas
        self.faiss_index = self._initialize_faiss_index()
        self.documents = self._load_documents()

        # Configurar OpenAI API
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def _initialize_faiss_index(self):
        # Inicializa un índice FAISS vacío
        return faiss.IndexFlatL2(384)  # Dimensión del modelo de embeddings

    def _load_documents(self):
        # Documentos iniciales de ejemplo (puedes cargar datos previos si ya tienes)
        return []

    def _embed_text(self, text):
        # Genera embeddings del texto usando Sentence Transformers
        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding

    def _ingest_external_data(self):
        # Fuente externa: NewsAPI
        api_key = os.getenv("NEWSAPI_KEY")
        url = f"https://newsapi.org/v2/everything?q=PYMEs&language=es&pageSize=5&apiKey={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            news = response.json().get("articles", [])
            for article in news:
                content = article.get("title", "") + " " + article.get("description", "")
                embedding = self._embed_text(content)
                self.faiss_index.add(np.array([embedding]).astype("float32"))
                self.documents.append({"content": content})
        else:
            raise Exception(f"Error al obtener datos externos: {response.status_code}")

    def post(self):
        # Parsear los argumentos de la solicitud
        args = self.parser.parse_args()
        query = args["query"]

        try:
            # Ingestar datos externos
            self._ingest_external_data()

            # Buscar documentos relevantes con FAISS
            relevant_docs = self._retrieve_relevant_documents(query)

            # Generar una respuesta creativa basada en los documentos relevantes
            response = self._generate_creative_answer(query, relevant_docs)
            return {"response": response}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def _retrieve_relevant_documents(self, query):
        # Obtener embedding de la consulta
        query_embedding = np.array([self._embed_text(query)]).astype("float32")

        # Buscar los documentos más cercanos
        distances, indices = self.faiss_index.search(query_embedding, k=3)  # Top 3 documentos relevantes
        relevant_docs = [self.documents[i]["content"] for i in indices[0]]
        return relevant_docs

    def _generate_creative_answer(self, query, relevant_docs):
        # Combinar documentos relevantes para proporcionar contexto
        context = "\n".join(relevant_docs)

        # Generar una respuesta usando el modelo GPT
        prompt = (
            f"Eres un asistente experto en estrategias de negocio para PYMEs. Basándote en la información de contexto proporcionada, proporciona soluciones prácticas, datos relevantes y recomendaciones personalizadas que ayuden a las pequeñas y medianas empresas a superar desafíos, aprovechar oportunidades y optimizar sus operaciones en áreas clave como la digitalización, la inteligencia artificial, el análisis de datos y la competitividad en el mercado:\n\n"
            f"{context}\n\n"
            f"Responde de manera creativa y útil a la siguiente pregunta:\n{query}"
        )

        response = openai.completions.create(
            prompt=prompt,
            max_tokens=300,
            temperature=0.7,
            model="gpt-3.5-turbo-instruct"
        )

        return response.choices[0].text.strip()
