import json

# Rutas completas de los archivos
archivos = [
    "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/routes/foda.py",
    "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/routes/marketing.py",
    "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/routes/predictions.py",
    "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/data/QA.json"
]

# Archivo de salida consolidado
archivo_salida = "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/routes/consolidado.py"

# Crear archivo consolidado
with open(archivo_salida, "w", encoding="utf-8") as salida:
    salida.write("# Archivo Consolidado\n\n")
    
    # Añadir los scripts Python
    for archivo in archivos[:-1]:  # Excluye QA.json por ahora
        with open(archivo, "r", encoding="utf-8") as f:
            salida.write(f"# Contenido de {archivo}\n")
            salida.write(f.read())
            salida.write("\n\n")
    
    # Añadir el archivo JSON como variable de Python
    salida.write("# Contenido de QA.json\n")
    with open(archivos[-1], "r", encoding="utf-8") as f:
        qa_data = json.load(f)
        salida.write("qa_data = ")
        json.dump(qa_data, salida, indent=4, ensure_ascii=False)

print(f"Archivo consolidado creado: {archivo_salida}")

