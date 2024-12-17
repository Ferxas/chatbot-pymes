from openai import OpenAI
import json
import os

# Configura el cliente de OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 1. Subir el archivo para fine-tuning
file_name = "mydata.jsonl"  # Archivo JSONL de ejemplos
print("Subiendo el archivo...")
file_response = client.files.create(
    file=open(file_name, "rb"),
    purpose="fine-tune"
)
file_id = file_response.id
print(f"Archivo subido exitosamente. File ID: {file_id}")

# 2. Crear un trabajo de fine-tuning
print("Creando trabajo de fine-tuning...")
fine_tune_response = client.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-4o-mini-2024-07-18",
)

fine_tune_job_id = fine_tune_response.id
print(
    f"Trabajo de fine-tuning creado exitosamente. Job ID: {fine_tune_job_id}")

# 3. Mostrar el ID del trabajo de fine-tuning
print("--- Resumen ---")
print(f"File ID: {file_id}")
print(f"Fine-tuning Job ID: {fine_tune_job_id}")

# Archivo JSONL de ejemplo
data = [
    {"messages": [
        {"role": "system", "content": "Eres un asistente de soporte."},
        {"role": "user", "content": "¿Cuál es el horario de atención?"},
        {"role": "assistant",
            "content": "Nuestro horario de atención es de 9 AM a 5 PM, de lunes a viernes."}
    ]},
    {"messages": [
        {"role": "system", "content": "Eres un asistente de soporte."},
        {"role": "user", "content": "¿Cómo puedo resetear mi contraseña?"},
        {"role": "assistant", "content": "Para resetear tu contraseña, visita la página de inicio de sesión y haz clic en \'¿Olvidaste tu contraseña?\'"}
    ]},
    {"messages": [
        {"role": "system", "content": "Eres un asistente de soporte."},
        {"role": "user", "content": "¿Dónde están ubicadas sus oficinas?"},
        {"role": "assistant", "content": "Nuestras oficinas están ubicadas en la Avenida Central #123, Ciudad Ejemplo."}
    ]}
]

# Guardar archivo JSONL de ejemplo
example_file = "example.jsonl"
with open(example_file, "w", encoding="utf-8") as f:
    for entry in data:
        f.write(json.dumps(entry) + "\n")
print(f"Archivo JSONL de ejemplo creado: {example_file}")
