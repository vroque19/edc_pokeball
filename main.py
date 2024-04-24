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

# global variables
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
outcomes = {
    "success": green,
    "fail": red
}

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

def get_pokemon():
    poke_map = {
        (147,200,208): "squirtle", # light blue
        (42,81,63): "bulbasaur", # bright green
        (254,148,65): "charmander", # orange
        (255, 255, 0): "pickachu" # yellow
    }
    items = list(poke_map.items())
    random_pokemon = random.choice(items)
    return random_pokemon


def play_sound(sound):
    with open("audio/"+sound+".wav", 'rb') as wave_file:
        print("\nplaying ", sound, "\n")
        wav = audiocore.WaveFile(wave_file)
        audio.play(wav)
        while audio.playing:
            pixels.fill(color)
            pixels.show()
        return
        
def flash(color, end):
    counter = 0
    while counter < end:
        print(color)
        pixels.fill(color)
        pixels.show()
        time.sleep(0.45)
        pixels.fill(black)
        pixels.show()
        time.sleep(0.45)
        counter += 1
    return
    
def flash_outcome(outcome):
    print(outcome)
    sound = "capture_"+outcome
    with open("audio/"+sound+".wav", 'rb') as wave_file:
        print("\nplaying ", sound, "\n")
        wav = audiocore.WaveFile(wave_file)
        audio.play(wav)
        while audio.playing:
            flash(white, 7)
            flash(outcomes[outcome], 3)
    return

def throw_pokeball(outcome, color, pokemon):
    print(outcome)
    flash_outcome(outcome)
    if outcome == "success":
        play_sound(pokemon)
    else:
        pass
    return
    
while True:
    outcome = random.choice(["success", "fail"])
    color, pokemon = get_pokemon()
    pixels.fill(white)
    pixels.show()
    if not button.value:  # button pressed
        print(color, pokemon)
        throw_pokeball(outcome, color, pokemon)
