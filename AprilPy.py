import cv2
from pyapriltags import Detector
from djitellopy import tello

detector = Detector(
    families="tag25h9",   # familia que quieres usar
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25
)

t = tello.Tello()
t.connect()
print("Batería:", t.get_battery())

t.streamoff()
t.streamon()
frame_reader = t.get_frame_read()

print("Leyendo cámara... (presiona Q para salir)")

t.takeoff()
t.move_down(35)
while True:
    frame = frame_reader.frame

    if frame is None:
        print("Frame vacío, esperando...")
        continue

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.rotate(img, cv2.ROTATE_180)
    img = cv2.flip(img, 1)

    detections = detector.detect(img)

    cv2.imshow("Tello - AprilTags", img)

    if len(detections) > 0:
        for det in detections:
            print("Detectado ID:", det.tag_id)

            # Aterrizar
            if det.tag_id in [1, 9]:
                print("Aterrizando...")
                t.land()
                break

            # Avanzar
            elif det.tag_id in [2, 11]:
                print("Avanzar")
                t.move_forward(20)

            # Giro 360
            elif det.tag_id in [0, 3]:
                print("Giro 360")
                t.rotate_clockwise(360)

            # Giro 180
            elif det.tag_id == 4:
                print("Giro 180")
                t.rotate_clockwise(180)

            # Izquierda 90
            elif det.tag_id == 5:
                print("Izquierda 90")
                t.rotate_counter_clockwise(90)

            # Derecha 90
            elif det.tag_id == 6:
                print("Derecha 90")
                t.rotate_clockwise(90)

            # Derecha 90
            elif det.tag_id in [7, 10]:
                print("Derecha 90")
                t.rotate_clockwise(90)

            # Izquierda 90
            elif det.tag_id == 8:
                print("Izquierda 90")
                t.rotate_counter_clockwise(90)

            t.move_forward(20)

        else:
            print("Sin detección: avanzando")
            t.move_forward(20)

        # Salir con Q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Aterrizando por comando del usuario")
            t.land()
            break

    # Salir con Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
t.streamoff()
