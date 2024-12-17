from flask_restful import Resource, reqparse
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import openai


class PredictionsResource(Resource):
    def __init__(self):
        # Parser para manejar datos de entrada
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "query", type=str, location="json", required=True, help="Query is required."
        )

        # Modelo para embeddings (FAISS)
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Configuración de FAISS para búsquedas rápidas
        self.faiss_index = self._initialize_faiss_index()
        self.documents = []

        # Configuración para OpenAI y fine-tuning
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Ruta absoluta al directorio de archivos .txt
        self.text_dir = os.path.abspath(os.path.join("C:/Users/ferxas/Documents/python/chatbot-pymes/data/txt"))
        self._ensure_text_directory()
        self._ingest_text_files(self.text_dir)

    def _ensure_text_directory(self):
        """
        Verifica que el directorio 'data/txt' exista. Si no, lanza un error.
        """
        if not os.path.exists(self.text_dir):
            raise Exception(f"El directorio '{self.text_dir}' no existe. Crea la carpeta y coloca archivos .txt dentro.")
        elif not os.listdir(self.text_dir):
            raise Exception(f"El directorio '{self.text_dir}' está vacío. Coloca archivos .txt para procesar.")

    def _initialize_faiss_index(self):
        # Inicializa un índice FAISS vacío
        return faiss.IndexFlatL2(384)  # Dimensión del modelo de embeddings

    def _embed_text(self, text):
        # Genera embeddings del texto usando Sentence Transformers
        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding

    def _ingest_text_files(self, text_dir):
        """
        Lee todos los archivos .txt en el directorio y actualiza el índice FAISS.
        """
        txt_files = [f for f in os.listdir(text_dir) if f.endswith(".txt")]
        if not txt_files:
            raise Exception(f"No se encontraron archivos .txt en la carpeta '{text_dir}'.")

        for txt_file in txt_files:
            file_path = os.path.join(text_dir, txt_file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Dividir el contenido en fragmentos manejables
            fragments = self._split_text_into_chunks(content)
            for fragment in fragments:
                embedding = self._embed_text(fragment)
                self.faiss_index.add(np.array([embedding]).astype("float32"))
                self.documents.append({"content": fragment, "source": txt_file})

    def _split_text_into_chunks(self, text, chunk_size=500):
        """
        Divide un texto largo en fragmentos de tamaño máximo `chunk_size`.
        """
        words = text.split()
        return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    def post(self):
        # Parsear los argumentos de la solicitud
        args = self.parser.parse_args()
        query = args["query"]

        try:
            # Buscar documentos relevantes con FAISS
            relevant_docs = self._retrieve_relevant_documents(query)

            # Generar una respuesta basada en fine-tuning y RAG
            response = self._generate_rag_answer(query, relevant_docs)
            return {"response": response}, 200
        except Exception as e:
            # Capturar y devolver errores específicos
            return {"error": str(e)}, 500

    def _retrieve_relevant_documents(self, query):
        # Validar si FAISS tiene datos
        if self.faiss_index.ntotal == 0:
            raise Exception("El índice FAISS está vacío. No se han cargado documentos.")

        # Obtener embedding de la consulta
        query_embedding = np.array([self._embed_text(query)]).astype("float32")

        # Buscar los documentos más cercanos
        distances, indices = self.faiss_index.search(query_embedding, k=3)  # Top 3 documentos relevantes

        # Validar que se encontraron documentos relevantes
        if len(indices[0]) == 0 or indices[0][0] == -1:
            raise Exception("No se encontraron documentos relevantes para la consulta.")

        # Recuperar documentos relevantes
        relevant_docs = [self.documents[i]["content"] for i in indices[0] if i != -1]
        return relevant_docs

    def _generate_rag_answer(self, query, relevant_docs):
        # Combinar documentos relevantes para proporcionar contexto
        context = "\n".join(relevant_docs)

        # Llamar al modelo fine-tuneado en OpenAI
        prompt = (
            f"Eres un asistente experto en estrategias de negocio para PYMEs. Basándote en la información de contexto proporcionada, proporciona soluciones prácticas, datos relevantes y recomendaciones personalizadas que ayuden a las pequeñas y medianas empresas a superar desafíos, aprovechar oportunidades y optimizar sus operaciones en áreas clave como la digitalización, la inteligencia artificial, el análisis de datos y la competitividad en el mercado:\n\n"
            f"{context}\n\n"
            f"Responde de manera creativa y útil a la siguiente pregunta:\n{query}"
        )

        response = openai.completions.create(
            model="",  # Reemplazar con el ID de tu modelo fine-tuneado
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].text.strip()