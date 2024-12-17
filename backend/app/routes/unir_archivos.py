import json
import os

# Rutas completas de los archivos
archivos = [
    "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/routes/foda.py",
    "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/routes/marketing.py",
    "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/routes/predictions.py",
    "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/routes/QA.json"  # Ruta corregida
]

# Archivo de salida consolidado
archivo_salida = "C:/Users/Usuario/Desktop/Escritorio/botcamp_ia/master/chatbot-pymes/backend/app/routes/consolidado.py"

# Crear archivo consolidado
with open(archivo_salida, "w", encoding="utf-8") as salida:
    salida.write("# Archivo Consolidado\n\n")
    
    # Añadir los scripts Python
    for archivo in archivos[:-1]:  # Excluye QA.json por ahora
        if os.path.exists(archivo):
            print(f"Procesando archivo: {archivo}")
            salida.write(f"# Contenido de {archivo}\n")
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()
                salida.write(contenido)
            salida.write("\n\n")
        else:
            print(f"Error: No se encontró el archivo {archivo}")
    
    # Añadir el archivo JSON como variable de Python
    if os.path.exists(archivos[-1]):
        print(f"Procesando archivo JSON: {archivos[-1]}")
        salida.write("# Contenido de QA.json\n")
        with open(archivos[-1], "r", encoding="utf-8") as f:
            qa_data = json.load(f)
            salida.write("qa_data = ")
            json.dump(qa_data, salida, indent=4, ensure_ascii=False)
        salida.write("\n\n")
    else:
        print(f"Error: No se encontró el archivo {archivos[-1]}")

print(f"\nArchivo consolidado creado correctamente en: {archivo_salida}")

