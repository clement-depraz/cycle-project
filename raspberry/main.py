import speech_recognition as sr
import pygame

from time import sleep
from fuzzywuzzy import fuzz
import numpy as np
from PIL import Image
import traceback
from led import display_led, shutdown_led
from movement import init_motion_sensor, detect_move
import tflite_runtime.interpreter as tflite
from utils import syntethise, take_picture

def predict_contener():
    im = Image.open('trash.jpg')
    im_resized = im.resize((120,120))
    data = list(im_resized.getdata())
    arr = np.asarray(data, dtype="float32") 
    arr = np.reshape(arr, (1, 120, 120, 3))
    interpreter = tflite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_data = arr
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()
    tflite_results = interpreter.get_tensor(output_details[0]['index'])
    print(tflite_results)
    return np.argmax(tflite_results)


def scenario_1():
    pygame.mixer.music.load("sounds/voice/start.mp3")
    pygame.mixer.music.play()
    pygame.time.delay(3000)
    take_picture()
    pred = predict_contener()
    syntethise(pred)

if __name__ == "__main__" :
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
                pass