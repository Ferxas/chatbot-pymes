import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Función para leer el archivo de texto
def leer_archivo_txt(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return archivo.read()

# Función para dividir el texto en fragmentos
def dividir_texto_en_fragmentos(texto, tamano_fragmento=1500):
    palabras = texto.split()
    return [" ".join(palabras[i:i + tamano_fragmento]) for i in range(0, len(palabras), tamano_fragmento)]

# Función para generar preguntas y respuestas para cada fragmento
def generar_preguntas_respuestas_por_fragmento(fragmento):
    preguntas_respuestas = []
    
    # Generar preguntas
    response_preguntas = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un generador de preguntas experto."},
            {"role": "user", "content": f"Genera 5 preguntas basadas en el siguiente texto:\n\n{fragmento}"}
        ],
        temperature=0.6,
        max_tokens=512
    )
    preguntas = response_preguntas.choices[0].message.content.strip().split("\n")
    
    # Generar respuestas
    for pregunta in preguntas:
        if pregunta.strip():
            response_respuestas = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Responde como un experto en el texto proporcionado."},
                    {"role": "user", "content": f"Responde a la siguiente pregunta basada en el texto:\n\nTexto: {fragmento}\n\nPregunta: {pregunta}"}
                ],
                temperature=0.7,
                max_tokens=512
            )
            respuesta = response_respuestas.choices[0].message.content.strip()
            preguntas_respuestas.append((pregunta, respuesta))
    
    return preguntas_respuestas

# Ruta al archivo
ruta_txt = "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/data/combinado/PDFCombinado.txt"

# Leer el texto
texto_completo = leer_archivo_txt(ruta_txt)
fragmentos = dividir_texto_en_fragmentos(texto_completo, tamano_fragmento=1500)

# Generar preguntas y respuestas para cada fragmento
preguntas_respuestas_totales = []
for i, fragmento in enumerate(fragmentos, start=1):
    print(f"Procesando fragmento {i}/{len(fragmentos)}...")
    preguntas_respuestas_totales.extend(generar_preguntas_respuestas_por_fragmento(fragmento))

# Guardar preguntas y respuestas en un archivo
archivo_salida = "preguntas_respuestas.txt"
with open(archivo_salida, "w", encoding="utf-8") as archivo:
    for pregunta, respuesta in preguntas_respuestas_totales:
        archivo.write(f"Pregunta: {pregunta}\nRespuesta: {respuesta}\n\n")

print(f"Preguntas y respuestas generadas y guardadas en {archivo_salida}")



