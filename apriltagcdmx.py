import cv2
from robotpy_apriltag import AprilTagDetector
from djitellopy import tello
import time

detector = AprilTagDetector()
detector.addFamily("tag36h11")

t = tello.Tello()
t.connect()
print("Batería:", t.get_battery())

t.streamoff()
t.streamon()
frame_reader = t.get_frame_read()

#RCCONTROL
def avanzar():
    #puedes mover velocidad pero no max de 25
    t.send_rc_control(0, 15, 0, 0)

def detener():
    t.send_rc_control(0, 0, 0, 0)

def giro_izquierda(grados):
    t.rotate_counter_clockwise(grados)

def giro_derecha(grados):
    t.rotate_clockwise(grados)

t.takeoff()
time.sleep(1)

print("Iniciando búsqueda de AprilTags...")

while True:
    frame = frame_reader.frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Correcciones de orientación
    gray = cv2.rotate(gray, cv2.ROTATE_180)
    gray = cv2.flip(gray, 1)

    detections = detector.detect(gray)

    if len(detections) > 0:
        id = detections[0].getId()
        print("Detectado ID:", id)

        if id in [1, 9]:
            detener()
            t.land()
            break

        elif id in [2, 11]:
            avanzar()

        elif id in [0, 3]:
            giro_derecha(360)

        elif id == 4:
            giro_derecha(180)

        elif id == 5:
            giro_izquierda(90)

        elif id == 6:
            giro_derecha(90)

        elif id in [7, 10]:
            giro_derecha(90)

        elif id == 8:
            giro_izquierda(90)

        avanzar()

    else:
        avanzar()

    cv2.imshow("Tello", gray)
    if cv2.waitKey(1) == ord('q'):
        detener()
        t.land()
        break

    time.sleep(0.05)

