
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.virtual import viewport
from luma.core.legacy.font import proportional, LCD_FONT
from time import sleep
import argparse

def display_led(catg):

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, width=8, height=8, rotate=3, block_orientation=0)
    with canvas(device) as draw:
        if catg == 0:
            text(draw, (0, 0), "M", fill="white")
        elif catg == 1:
            text(draw, (0, 0), "V", fill="white")
        elif catg == 2:
            text(draw, (0, 0), "J", fill="white")
        elif catg == 3:
            text(draw, (0, 0), "B", fill="white")
    sleep(2)

def shutdown_led():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, width=8, height=8, rotate=3, block_orientation=0)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box,  outline="black", fill="black")



