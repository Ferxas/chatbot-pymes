import os
import openai
from dotenv import load_dotenv

# Cargar clave API desde .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verificar clave API
if not openai.api_key:
    print("Error: La clave de API no está configurada. Verifica tu archivo .env.")
    exit()

# Ruta del archivo JSONL
file_path = "../models/train.jsonl"  # Ajusta la ruta del archivo JSONL

# Verificar que el archivo existe
if not os.path.exists(file_path):
    print(f"Error: El archivo JSONL no se encontró en la ruta: {file_path}")
    exit()

# Subir el archivo para fine-tuning
print("Subiendo el archivo para fine-tuning...")
try:
    with open(file_path, "rb") as f:
        response = openai.File.create(file=f, purpose="fine-tune")
    file_id = response.get("id")
    print(f"Archivo subido con éxito. File ID: {file_id}")
except Exception as e:
    print(f"Error al subir el archivo: {e}")
    exit()

# Probar el modelo fine-tuneado (reemplaza con tu modelo entrenado)
print("\nProbando el modelo fine-tuneado...")
try:
    response = openai.completions.create(
        model="ftjob-jWoP7IiKGiPoDuzx0nOpGPoB",  # Reemplaza con tu ID de modelo
        prompt="¿Cuál es el papel de las PYME en la economía de España?",
        max_tokens=100
    )
    print("Respuesta del modelo fine-tuneado:")
    print(response["choices"][0]["text"].strip())
except Exception as e:
    print(f"Error al probar el modelo: {e}")

