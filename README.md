Sistema Automatizado de Clasificación de Piezas LEGO con CNN

Un sistema automatizado que utiliza visión artificial y robótica para clasificar piezas LEGO en dos categorías principales: bloques y minifiguras. Este proyecto soluciona el lento proceso manu
al de clasificación mediante la integración de hardware, actuadores mecánicos y modelos de Deep Learning.

Arquitectura del Sistema

Debido a las limitaciones de velocidad de procesamiento nativo en la Raspberry Pi, el proyecto implementa una arquitectura distribuida tipo cliente-servidor:

Captura y Transmisión: Una cámara conectada a la Raspberry Pi captura video en vivo a resolución 320x240 y lo transmite a una laptop local a través de la librería imagezmq.

Procesamiento IA: El servidor (laptop) recibe los fotogramas y ejecuta un modelo YOLO (2ndlegomodel.pt) para identificar los objetos.

Retorno de Señal: El servidor envía un comando estricto de vuelta a la Raspberry Pi (A para bloques, B para minifiguras), la cual activa los pines GPIO 26 o 13 respectivamente.

Clasificación Mecánica: Un Arduino lee estas señales y gestiona los motores. Utiliza un sensor ultrasónico para detectar cuando una pieza está a 5 cm o menos, deteniendo el motor DC de la banda transportadora. Finalmente, un servomotor posiciona una rampa direccional a 45° para bloques o a 125° para minifiguras, arrojando la pieza a su caja de almacenamiento designada.

Clasificación y Modelo

La Red Neuronal Convolucional (CNN) fue entrenada con más de 150 imágenes, logrando una precisión superior al 80% en la detección. El modelo reconoce las siguientes clases:

Stack Tecnológico

Hardware:Raspberry Pi + Módulo de Cámara.   
Placa Arduino.   
Banda transportadora impulsada por un Motor DC.   
Servomotor para rampa direccionable.   
Sensor Ultrasónico (Trigger/Echo) para detección de proximidad. 

Software:Lenguajes: Python (Raspberry Pi y Servidor IA), C++ (Lógica de Arduino).

Librerías principales: ultralytics (YOLO), OpenCV, imagezmq, picamera2, gpiozero.

Instalación y Configuración
1. Configuración de Red:
Ambos dispositivos deben estar en la misma red local.
SSID: Lego.
Contraseña: 12345678.

2. Credenciales de la Raspberry Pi:
Usuario: admin.
Contraseña: lego123.

3. Ejecución del Servidor (Laptop):
La laptop debe tener la dirección IP estática 192.168.137.1. Ejecuta el script del cerebro de IA para poner el servidor en escucha:python servidor_ia.py

4. Ejecución del Cliente (Raspberry Pi):
Inicia el script de transmisión y recepción de GPIO en la Raspberry Pi: python3 cliente_final.py
(Nota: Para apagar la placa de forma segura tras su uso, ejecuta sudo poweroff).

Uso
Coloca una pieza LEGO en la banda transportadora.

Observa la ventana de visualización de OpenCV generada por el servidor IA.

Presiona la tecla [ESPACIO] para que la IA realice una captura y predicción manual sobre el objeto en pantalla.

El sistema automatizado se encargará de detener la banda, mover el servomotor a la posición correcta, volver a encender la banda por 3 segundos para arrojar la pieza, y reiniciar el ciclo a su posición original (90°).

Para salir del servidor, presiona la tecla [ESC].
