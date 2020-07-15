import speech_recognition as sr
import pygame
from time import sleep, time
from fuzzywuzzy import fuzz
import numpy as np
from PIL import Image
import traceback
import requests
from utils import syntethise, take_picture_aws
from led import shutdown_led

def send_image(path, category):
    with open(path, 'rb') as img:
        image = {'image': img}
        with requests.Session() as s:
            url = "http://ec2-34-254-248-190.eu-west-1.compute.amazonaws.com:80/image/new?type=" + category
            r = s.post(url,files=image)
            print(r.status_code)

def scenario_2():
    shutdown_led()
    photo_name = take_picture_aws()

    pygame.mixer.init()
    r = sr.Recognizer()
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/voice/scenario2.mp3")
    done = False
    i = 0
    while done == False:
        if i == 0 or i % 10 == 0:
            pygame.mixer.music.play()
            pygame.time.delay(11000)
        with sr.Microphone() as src:
            print("speak")
            try:
                audio = r.listen(src, 2, 2)
                print(type(audio))
                print("end")
                text = r.recognize_google(audio, language='fr-FR')
                print(text)
                print("TEXT " + text)
                if (fuzz.ratio(text, "jaune")) > 70:
                    print("jaune")
                    send_image(photo_name, "recyclable")
                    syntethise(2)
                    done = True
                elif (fuzz.ratio(text, "verte")) > 70:
                    print("verte")
                    send_image(photo_name, "organique")
                    syntethise(1)
                    done = True
                elif (fuzz.ratio(text, "marron")) > 70:
                    print("marron")
                    send_image(photo_name, "autre")
                    syntethise(0)
                    done = True
                elif (fuzz.ratio(text, "bleu")) > 70:
                    print("bleu")
                    send_image(photo_name, "verre")
                    syntethise(3)
                    done = True
                elif (fuzz.ratio(text, "je ne sais pas")) > 70:
                    print("je ne sais pas")
                    send_image(photo_name, "inconnu")
                    syntethise(0)
                    done = True
            except Exception:
                pass
        i += 1
        print(i)

if __name__ == "__main__" :
    scenario_2()