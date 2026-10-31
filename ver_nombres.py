from ultralytics import YOLO

# CAMBIA ESTO por el nombre real de tu archivo
nombre_del_archivo = "2ndlegomodel.pt" 

try:
    # Cargar el modelo
    model = YOLO(nombre_del_archivo)
    
    # Imprimir el diccionario de nombres
    print("\n--- LISTA DE CLASES DETECTADAS ---")
    print(model.names)
    print("----------------------------------\n")
    
except Exception as e:
    print(f"Error: {e}")
    print("Asegúrate de que el nombre del archivo sea correcto y esté en la misma carpeta.")