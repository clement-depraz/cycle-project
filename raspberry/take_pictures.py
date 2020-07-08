from picamera import PiCamera
from time import sleep

item = "mousse"

with PiCamera() as camera:
    camera.start_preview()
    camera.rotation = 90
    camera.resolution = (640, 480)
    for i in range(0, 50):
        sleep(1)
        #my_file = open("dataset/" + item + "_" + str(i) + ".jpg", 'wb')
        camera.capture("dataset/" + item + "_" + str(i) + ".jpg")