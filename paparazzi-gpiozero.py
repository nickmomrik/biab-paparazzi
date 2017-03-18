#!/usr/bin/python

from gpiozero import DistanceSensor, LightSensor, Button, LED
from time import sleep
from datetime import datetime
from signal import pause
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
ULTRASONIC_MAX_DIST = 1.8
ULTRASONIC_DIST = 1
PHOTOCELL_LIGHT = 0.2

ultrasonic = DistanceSensor(
	echo = ULTRASONIC_ECHO_PIN,
	trigger = ULTRASONIC_TRIG_PIN,
	max_distance = ULTRASONIC_MAX_DIST,
	threshold_distance = ULTRASONIC_DIST )
photocell = LightSensor(
	pin = PHOTOCELL_PIN,
	threshold = PHOTOCELL_LIGHT )
button = Button( BUTTON_PIN )
green = LED( BUTTON_LED_PIN )
red = LED( PHOTOCELL_LED_PIN )
blue = LED( ULTRASONIC_LED_PIN )

def take_picture_if_light( led, name ) :
	global photocell

	if ( photocell.light_detected ) :
		led.on()
		print( name )
		os.system( '/opt/bloginabox/biab camera-take-photo "' + datetime.now().strftime( '%-I:%M:%S %p' ) + ' - ' + name + '"' )
		sleep( 1 )
		led.off()

try :
	ultrasonic.when_in_range = lambda: take_picture_if_light( blue, 'Ultrasonic' )
	photocell.when_light = lambda: take_picture_if_light( red, 'Photocell' )
	button.when_pressed = lambda: take_picture_if_light( green, 'Button' )

	pause()

except KeyboardInterrupt :
	print 'Exiting via CTRL+C...'
