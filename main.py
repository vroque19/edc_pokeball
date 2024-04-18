# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import neopixel
import digitalio
import random
import audiocore
import audiobusio

# On a Raspberry pi, use this instead, not all pins are supported
pixel_pin = board.D10
# The number of NeoPixels
num_pixels = 12
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

button = digitalio.DigitalInOut(board.A3)
button.switch_to_input(pull=digitalio.Pull.UP)

audio = audiobusio.I2SOut(board.A0, board.A1, board.A2)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


counter = 0

while True:
    if not button.value:
        with open("daddys-home1.wav", "rb") as wave_file:
            wav = audiocore.WaveFile(wave_file)
            audio.play(wav)
            while audio.playing:
                pass
        while counter < 3:
            pixels.fill((255, 255, 255))
            pixels.show()
            time.sleep(0.1)
            pixels.fill((0, 0, 0))
            pixels.show()
            time.sleep(0.1)
            counter += 1
    else:
        pixels.fill((0, 255, 0))
    pixels.show()
