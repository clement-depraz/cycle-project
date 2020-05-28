import speech_recognition as sr
import pygame
from picamera import PiCamera
from time import sleep
from fuzzywuzzy import fuzz
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image

def syntethise(contener_id):
    pygame.mixer.init()

    if contener_id == 0:
        pygame.mixer.music.load("sounds/generated/poubelle_autre.mp3")
        pygame.mixer.music.play()
    elif contener_id == 1:
        pygame.mixer.music.load("sounds/generated/poubelle_organique.mp3")
        pygame.mixer.music.play()
    elif contener_id == 2:
        pygame.mixer.music.load("sounds/generated/poubelle_recyclage.mp3")
        pygame.mixer.music.play()
    elif contener_id == 3:
        pygame.mixer.music.load("sounds/generated/poubelle_verre.mp3")
        pygame.mixer.music.play()
    pygame.time.delay(15000)
    pygame.mixer.music.load("sounds/generated/merci.mp3")
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
    pygame.mixer.music.load("sounds/generated/photo.mp3")
    pygame.mixer.music.play()
    pygame.time.delay(5000)
    camera = PiCamera()
    sleep(5)
    camera.capture("trash.jpg")
    
if __name__ == "__main__" :
    r = sr.Recognizer()
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/generated/intro.mp3")
    while (1):
        with sr.Microphone() as src:
            print("speak")
            audio = r.listen(src)
            print(type(audio))
            print("end")

            try:
                text = r.recognize_google(audio, language='fr-FR')
                print(text)
                print("TEXT " + text)
                ratio = fuzz.ratio(text, "ok cycle")
                if ratio > 50:
                    pygame.mixer.music.play()
                    pygame.time.delay(5000)
                    take_picture()
                    pred = predict_contener()
                    syntethise(pred)

            except:
                print("error")
                pass