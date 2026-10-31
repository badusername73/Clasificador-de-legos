import time
import imagezmq
import socket
import cv2
import numpy as np
from picamera2 import Picamera2
from gpiozero import OutputDevice

# ================= CONFIGURACIÓN =================
ip_laptop = '192.168.137.1'  # REVISA QUE LA IP NO HAYA CAMBIADO

# Pines GPIO
pin_A = OutputDevice(26, initial_value=False) # Bloques
pin_B = OutputDevice(13, initial_value=False) # Minifiguras

print("✅ Modo: VIDEO EN VIVO + FILTRO ESTRICTO.")

# ================= INICIAR CÁMARA =================
try:
    print("📷 Iniciando cámara...")
    rpi_name = socket.gethostname()
    sender = imagezmq.ImageSender(connect_to=f'tcp://{ip_laptop}:5555')

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (320, 240), "format": "RGB888"})
    picam2.configure(config)
    picam2.start()

    print(f"🚀 Transmitiendo a {ip_laptop}...")
    print("   El robot solo se moverá si recibe 'A' o 'B'.")

    while True:
        # 1. Capturar frame
        frame = picam2.capture_array()
        
        # 2. Enviar a la laptop y esperar respuesta
        respuesta_bytes = sender.send_image(rpi_name, frame)
        
        # .strip() elimina espacios en blanco invisibles que causan errores
        orden = respuesta_bytes.decode("utf-8").strip()
        
        # 3. FILTRO ESTRICTO DE ÓRDENES
        if orden == 'A':
            print("🚨 ¡ORDEN RECIBIDA! -> CLASIFICANDO BLOQUE (A)")
            pin_A.on()
            time.sleep(0.5) # Pulso de medio segundo
            pin_A.off()
            
        elif orden == 'B':
            print("🚨 ¡ORDEN RECIBIDA! -> CLASIFICANDO MINIFIGURA (B)")
            pin_B.on()
            time.sleep(0.5) 
            pin_B.off()
            
        else:
            # Si recibe "OK", "N" o cualquier otra cosa, NO HACE NADA.
            # Imprimimos un punto para saber que sigue vivo sin llenar la pantalla
            print(".", end="", flush=True) 

except KeyboardInterrupt:
    print("\n🛑 Detenido por usuario.")
except Exception as e:
    print(f"❌ Error: {e}")

finally:
    picam2.stop()
    pin_A.off()
    pin_B.off()
    print("🏁 Fin.")