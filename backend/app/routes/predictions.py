from flask_restful import Resource, reqparse
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch

class PredictionsResource(Resource):
    def __init__(self):
        # Parser para manejar datos de entrada
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("query", type=str, location="json", required=True, help="Query is required.")

        # Modelo para generar embeddings
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Configuración de FAISS para búsquedas rápidas
        self.faiss_index = self._initialize_faiss_index()
        self.documents = self._load_documents()

    def _initialize_faiss_index(self):
        # Inicializa un índice FAISS vacío
        return faiss.IndexFlatL2(384)  # Dimensión del modelo de embeddings

    def _load_documents(self):
        # Documentos de ejemplo (puedes reemplazar con datos reales)
        documents = [
            {"id": 1, "content": "Las ventas trimestrales han aumentado un 15% en comparación con el año pasado."},
            {"id": 2, "content": "El mercado de tecnología muestra un crecimiento exponencial en el último semestre."},
            {"id": 3, "content": "Las campañas de marketing digital han generado un ROI positivo del 20%."}
        ]

        # Crear embeddings para cada documento y añadirlos a FAISS
        embeddings = [self._embed_text(doc["content"]) for doc in documents]
        self.faiss_index.add(np.array(embeddings).astype("float32"))

        return documents

    def _embed_text(self, text):
        # Genera embeddings del texto usando Sentence Transformers
        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding

    def post(self):
        # Parsear los argumentos de la solicitud
        args = self.parser.parse_args()
        query = args["query"]

        try:
            # Buscar documentos relevantes con FAISS
            relevant_docs = self._retrieve_relevant_documents(query)

            # Generar respuesta usando los documentos relevantes
            response = self._generate_answer(query, relevant_docs)
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

    def _generate_answer(self, query, relevant_docs):
        # Combinar documentos relevantes para proporcionar contexto
        context = " ".join(relevant_docs)
        return {"context": context}