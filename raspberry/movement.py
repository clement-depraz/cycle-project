import  RPi.GPIO as GPIO
import time


def init_motion_sensor():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(11, GPIO.IN) 



def detect_move():
    move = GPIO.input(11)
    print(move)
    time.sleep(0.1)
    return move
