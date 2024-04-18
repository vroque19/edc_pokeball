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
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

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


def flash(outcome, color, pokemon):
    counter = 0
    while counter < 3:
        print("white")
        pixels.fill((255, 255, 255))
        pixels.show()
        time.sleep(0.45)
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.45)
        counter += 1
    if outcome == "success":
        flash_success(color, pokemon)
    else:
        flash_fail(pokemon)

def get_pokemon():
    poke_map = {
        (64, 164, 223): "squirtle", # light blue
        (51, 102, 49): "bulb", # bright green
        (255, 165, 0): "char" # orange
    }
    items = list(poke_map.items())
    random_pokemon = random.choice(items)
    return random_pokemon


def flash_success(color, pokemon):
    print("successfully caught ", pokemon, "!\n")
    # play capture + success audio
    counter = 0
    while counter < 5:
        time.sleep(0.2)
        pixels.fill((0, 255, 0)) # green
        pixels.show()
        time.sleep(0.2)
        pixels.fill((0, 0, 0))
        pixels.show()
        counter += 1
    counter = 0
    while counter < 1000:
        pixels.fill(color)
        pixels.show()
        counter += 1
    return
    # play pokemon audio



def flash_fail(pokemon):
    print("did not catch ", pokemon, "!\n")
    counter = 0
    #play the capture+fail sound
    while counter < 5:
        time.sleep(0.5)
        pixels.fill((255, 0, 0)) # red
        pixels.show()
        time.sleep(0.5)
        pixels.fill((0, 0, 0))
        pixels.show()
        counter += 1


while True:
    outcome = random.choice(["success", "fail"])
    pixels.fill((0, 0, 0))
    pixels.show()
    if not button.value:  # button pressed
        color, pokemon = get_pokemon()
        print(color, pokemon)
        flash(outcome, color, pokemon)


