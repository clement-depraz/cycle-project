import speech_recognition as sr
import pygame
from picamera import PiCamera
from time import sleep
from fuzzywuzzy import fuzz
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.virtual import viewport
from luma.core.legacy.font import proportional, LCD_FONT
import traceback
from led import display_led, shutdown_led
from movement import init_motion_sensor, detect_move

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


def predict_contener():
    im = Image.open('trash.jpg')
    im_resized = im.resize((112,112))
    data = list(im_resized.getdata())
    arr = np.asarray(data, dtype="float32") 
    arr = np.reshape(arr, (1, 112, 112 , 3))
    interpreter = tflite.Interpreter(model_path="cycle_model_CNN_mk1.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_data = arr
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()
    tflite_results = interpreter.get_tensor(output_details[0]['index'])
    return np.argmax(tflite_results)

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

def scenario_1():
    pygame.mixer.music.load("sounds/voice/start.mp3")
    pygame.mixer.music.play()
    pygame.time.delay(3000)
    take_picture()
    pred = predict_contener()
    syntethise(pred)

if __name__ == "__main__" :
    #syntethise(1)
    r = sr.Recognizer()
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/voice/start.mp3")
    init_motion_sensor()
    while (1):
        shutdown_led()
        if detect_move() == 1:
            scenario_1()
        with sr.Microphone() as src:
            print("speak")
            try:
                audio = r.listen(src, 0.5, 2)
                print(type(audio))
                print("end")
                text = r.recognize_google(audio, language='fr-FR')
                print(text)
                print("TEXT " + text)
                ratio = fuzz.ratio(text, "ok cycle")
                if ratio > 70:
                    scenario_1()

            except Exception:
                #traceback.print_exc()
                pass