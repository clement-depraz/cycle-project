from time import sleep, time
from led import display_led, shutdown_led
import pygame
from picamera import PiCamera

def syntethise(contener_id):
    display_led(contener_id)
    if contener_id == 0:
        pygame.mixer.music.load("sounds/voice/poubelle_marron.mp3")
        pygame.mixer.music.play()
    elif contener_id == 1:      
        pygame.mixer.music.load("sounds/voice/poubelle_verte.mp3")
        pygame.mixer.music.play()
    elif contener_id == 2:
        pygame.mixer.music.load("sounds/voice/poubelle_jaune.mp3")
        pygame.mixer.music.play()
    elif contener_id == 3:
        pygame.mixer.music.load("sounds/voice/poubelle_bleu.mp3")
        pygame.mixer.music.play()

    pygame.time.delay(5000)
    sleep(3)


def take_picture():
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/voice/photo.mp3")
    pygame.mixer.music.play()
    pygame.time.delay(4000)

    my_file = open('trash.jpg', 'wb')
    with PiCamera() as camera:
        camera.rotation = 90
        camera.resolution = (640, 480)
        camera.start_preview()
        sleep(3)
        camera.capture(my_file)
    my_file.close()

def take_picture_aws():
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/voice/photo.mp3")
    pygame.mixer.music.play()
    pygame.time.delay(4000)
    photo_name = " trash_" + str(time()) + ".png"
    my_file = open(photo_name, 'wb')
    with PiCamera() as camera:
        camera.rotation = 90
        camera.resolution = (640, 480)
        camera.start_preview()
        sleep(3)
        camera.capture(my_file)
    my_file.close()
    return photo_name