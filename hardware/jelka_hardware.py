#!/usr/bin/env python3
import jelka_config
from sys import argv
from os import getenv
from time import sleep
from rpi_ws281x import PixelStrip, Color

LED_PIN = 18					# GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000	# LED signal frequency in hertz (usually 800khz)
LED_DMA = 10					# DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255	# Set to 0 for darkest and 255 for brightest
LED_INVERT = False		# True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0				# set to '1' for GPIOs 13, 19, 41, 45 or 53

luči = jelka_config.luči
if getenv("LEDS"):
	luči = int(getenv("LEDS"))

strip = PixelStrip(luči, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def nastavi(luč, barva):
	strip.setPixelColor(luč, Color(barva[1], barva[0], barva[2]))

def izriši():
	strip.show()

if __name__ == '__main__':
	print(argv[0] + "hardware test ...")
	i = 0
	try:
		while True:
			for k in range(luči):
				if (i % 2 == 0):
					strip.setPixelColor(k, Color(255, 255, 255))
				else:
					strip.setPixelColor(k, Color(0, 0, 0))
			strip.show()
			time.sleep(0.1)
			i += 1
	except KeyboardInterrupt:
		pass
