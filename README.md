# Apriltags con DJI Tello 

Este proyecto implementa un sistema de navegación autónoma para el dron **DJI Tello**, utilizando **detección de AprilTags** para ejecutar acciones como giros, avance continuo o finalización del vuelo.

El dron **avanza indefinidamente** hasta detectar un nuevo AprilTag.  
Cada AprilTag activa una acción específica, permitiendo construir rutas o comportamientos 

#  ¿Quién soy?

Somos un equipo llamado Hyperion conformodad por  **Cinthya Nogales Badillo** ,**Evelyn Gamboa Mata**, estudiante de **Ingeniería en Ciencia de Datos y Matemáticas** y **Ingenieria en Mecatronica** en el Tecnológico de Monterrey, Campus Ciudad de México.  

#  ¿Por qué hice este código?

El objetivo del proyecto es crear un sistema donde un dron **DJI Tello** pueda:

- Navegar **solo**, sin control manual.  
- Leer **AprilTags** (códigos visuales parecidos a QR).  
- Ejecutar acciones específicas según el ID del tag.  
- Avanzar de manera continua hasta encontrar el siguiente tag.  

En pocas palabras:  
**Hice este código para que el dron pueda seguir instrucciones visuales y moverse de forma autónoma usando visión artificial.**

##  Acciones asignadas por ID

| ID | Acción |
|----|--------|
| **0** | Giro de 360° |
| **1** | Fin del vuelo (aterrizar) |
| **2** | Avanzar |
| **3** | Giro de 360° |
| **4** | Giro de 180° |
| **5** | Giro a la izquierda (90°) |
| **6** | Giro de 90° |
| **7** | Giro a la derecha (90°) |
| **8** | Giro a la izquierda (90°) |
| **9** | Fin del vuelo |
| **10** | Giro a la derecha (90°) |
| **11** | Avanzar |

Después de ejecutar cualquier acción, el dron **retoma el avance continuo**.

---

##  Comportamiento del dron

1. El dron despega.
2. Comienza a **avanzar continuamente** usando `send_rc_control`.
3. Cuando detecta un AprilTag:
   - Ejecuta la acción asignada al ID.
   - Vuelve a avanzar automáticamente.
4. Si detecta un ID de fin de vuelo (1 o 9), **aterriza inmediatamente**.
5. Si no detecta ningún tag, **sigue avanzando**.

---

##  Velocidad recomendada

El dron avanza con:

```python
t.send_rc_control(0, 15, 0, 0)
```

Esta velocidad (15-20 cm/s) es la más estable para detección continua porque:
- Reduce vibraciones.
- Evita que el dron pase de largo antes de detectar el tag.
- Mantiene el AprilTag dentro del campo de visión.

## Flujo del sistema
1. Captura de frame desde la cámara del Tello.
2. Conversión a escala de grises.
3. Corrección de orientación (rotación + flip).
4. Detección de AprilTags.
5. Ejecución de acción según ID.
6. Retorno al avance continuo.

## Dependencias
```python
djitellopy

robotpy_apriltag

opencv-python
```

