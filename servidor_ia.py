import cv2
import imagezmq
from ultralytics import YOLO

print("🧠 Cargando cerebro (Modo Manual)...")
try:
    model = YOLO('2ndlegomodel.pt') 
    print("✅ Modelo cargado.")
except:
    print("❌ ERROR: No encuentro el archivo .pt")
    exit()

image_hub = imagezmq.ImageHub()
print("📡 Servidor LISTO. Presiona [ESPACIO] para detectar.")

# Variable para saber si debemos detectar en este momento
detectar_ahora = False

while True:
    # 1. Recibir imagen
    rpi_name, image = image_hub.recv_image()
    
    comando_a_enviar = "OK" # Por defecto, decimos "Todo bien, sigue grabando"
    
    # 2. ¿El usuario presionó el botón?
    if detectar_ahora:
        print("📸 ¡Captura solicitada! Analizando...")
        
        # --- AQUÍ ENTRA LA IA ---
        results = model.predict(image, conf=0.5, verbose=False)
        
        if len(results[0].boxes) > 0:
            box = results[0].boxes[0]
            clase_id = int(box.cls[0])
            nombre_clase = model.names[clase_id]
            
            # Lógica de clasificación
            if nombre_clase in ['baseplate', 'big_lego', 'slim_lego', 'small_lego']:
                comando_a_enviar = "A"
                print(f"   -> Detectado: BLOQUE ({nombre_clase})")
            elif nombre_clase == 'minifigure':
                comando_a_enviar = "B"
                print(f"   -> Detectado: MINIFIGURA")
        else:
            comando_a_enviar = "N"
            print("   -> No vi nada claro.")
            
        # Dibujamos las cajas para que veas qué detectó
        image = results[0].plot()
        
        # Apagamos el "gatillo" para que no siga detectando a lo loco
        detectar_ahora = False 

    # 3. Enviar la respuesta a la Raspberry Pi
    image_hub.send_reply(comando_a_enviar.encode())
    
    # 4. Mostrar video en pantalla
    cv2.imshow("Vista del Robot (ESPACIO para foto)", image)

    # 5. Leer teclado
    key = cv2.waitKey(1)
    if key == 27: # Tecla ESC para salir
        break
    elif key == 32: # Tecla ESPACIO (Código 32)
        detectar_ahora = True
        print(">> Solicitud de detección iniciada...")

cv2.destroyAllWindows()