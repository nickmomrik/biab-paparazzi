#!/usr/bin/python

from gpiozero import DistanceSensor, LightSensor, Button, LED
from datetime import datetime
from signal import pause
from time import sleep
import os

# GPIO PINS
BUTTON_PIN          = 23
BUTTON_LED_PIN      = 5
PHOTOCELL_PIN       = 18
PHOTOCELL_LED_PIN   = 6
ULTRASONIC_TRIG_PIN = 20
ULTRASONIC_ECHO_PIN = 21
ULTRASONIC_LED_PIN  = 13

# TEST CONSTANTS
ULTRASONIC_MAX  = 1.5625
ULTRASONIC_DIST = 1.1
PHOTOCELL_LIGHT = 0.1
PHOTOCELL_QUEUE = 5
PHOTOCELL_LIMIT = 0.02

# SENSORS
button = Button( BUTTON_PIN )
photocell = LightSensor(
	pin = PHOTOCELL_PIN,
	threshold = PHOTOCELL_LIGHT,
	queue_len = PHOTOCELL_QUEUE,
	charge_time_limit = PHOTOCELL_LIMIT )
ultrasonic = DistanceSensor(
	echo = ULTRASONIC_ECHO_PIN,
	trigger = ULTRASONIC_TRIG_PIN,
	max_distance = ULTRASONIC_MAX,
	threshold_distance = ULTRASONIC_DIST )

# LED for each sensor
green = LED( BUTTON_LED_PIN )
red   = LED( PHOTOCELL_LED_PIN )
blue  = LED( ULTRASONIC_LED_PIN )

def take_picture_if_light( led, name, light = False ) :
	global photocell

	if ( ( light or photocell.light_detected ) and not taking_picture() ) :
		led.on()
		os.system( '/opt/bloginabox/biab camera-take-photo "' + datetime.now().strftime( '%-I:%M:%S %p' ) + ' - ' + name + '"' )
		led.off()

def taking_picture() :
	return green.is_lit or red.is_lit or blue.is_lit

try :
	ultrasonic.when_in_range = lambda: take_picture_if_light( blue, 'Ultrasonic' )
	photocell.when_light = lambda: take_picture_if_light( red, 'Photocell', True )
	button.when_pressed = lambda: take_picture_if_light( green, 'Button' )

	pause()
except KeyboardInterrupt :
	print( ' Exiting via CTRL+C...' )
