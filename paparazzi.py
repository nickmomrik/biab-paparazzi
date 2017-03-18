#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from datetime import datetime
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
LIGHT_MIN        = 100
PHOTOCELL_LIGHT  = 50
PHOTOCELL_DIFF   = 100
ULTRASONIC_DIST  = 100

GPIO.setmode( GPIO.BCM )

GPIO.setup( BUTTON_PIN, GPIO.IN )
GPIO.setup( BUTTON_LED_PIN, GPIO.OUT )
GPIO.setup( PHOTOCELL_LED_PIN, GPIO.OUT )
GPIO.setup( ULTRASONIC_TRIG_PIN, GPIO.OUT )
GPIO.setup( ULTRASONIC_ECHO_PIN, GPIO.IN )
GPIO.setup( ULTRASONIC_LED_PIN, GPIO.OUT )

GPIO.output( BUTTON_LED_PIN, GPIO.LOW )
GPIO.output( PHOTOCELL_LED_PIN, GPIO.LOW )
GPIO.output( ULTRASONIC_TRIG_PIN, GPIO.LOW )
GPIO.output( ULTRASONIC_LED_PIN, GPIO.LOW )

def take_picture( led_pin, title ) :
	GPIO.output( led_pin, GPIO.HIGH )
	title = datetime.now().strftime( '%-I:%M:%S %p' ) + ' - ' + title
	os.system( '/opt/bloginabox/biab camera-take-photo "' + title + '"' )
	GPIO.output( led_pin, GPIO.LOW )
	reset_prev_readings()

# https://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading
def read_photocell() :
	GPIO.setup( PHOTOCELL_PIN, GPIO.OUT )
	GPIO.output( PHOTOCELL_PIN, GPIO.LOW )
	time.sleep( 0.05 )
	GPIO.setup( PHOTOCELL_PIN, GPIO.IN )

	start = time.clock()
	while ( True ) :
		end = time.clock()
		if ( GPIO.input( PHOTOCELL_PIN ) == GPIO.HIGH ) :
			break

		# Speed things up if it's sufficiently dark
		if ( ( end - start ) > 0.2 ) :
			return 200

	return int( round( ( end - start ) * 1000 ) )

# https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
def read_ultrasonic() :
	# Trigger the sensor
	GPIO.output( ULTRASONIC_TRIG_PIN, GPIO.HIGH )
	time.sleep( 0.15 )
	GPIO.output( ULTRASONIC_TRIG_PIN, GPIO.LOW )

	# Read the sensor
	while ( True ) :
		start = time.clock()
		if ( GPIO.input( ULTRASONIC_ECHO_PIN ) == GPIO.HIGH ) :
			break
	while ( True ) :
		end = time.clock()
		if ( GPIO.input( ULTRASONIC_ECHO_PIN ) == GPIO.LOW ) :
			break

	diff = end - start
	if ( diff > 0.2 ) :
		value = -1
	else :
		value = int( round( diff * 17150 ) )

	return value

def is_light_enough() :
	return ( prev_photocell[2] != -1 and prev_photocell[3] != -1
		and prev_photocell[2] < LIGHT_MIN and prev_photocell[3] < LIGHT_MIN )

def is_button_triggered() :
	global prev_button

	button = GPIO.input( BUTTON_PIN )

	if ( is_light_enough()
			and GPIO.LOW == button and GPIO.HIGH == prev_button ) :
		prev_button = button
		return True

	return False

def is_photocell_triggered() :
	global prev_photocell

	# Take 4 readings
	for i in range( 1, 4 ):
		photocell = read_photocell()
		# Shift readings
		prev_photocell = ( prev_photocell[1], prev_photocell[2], prev_photocell[3], photocell )
		new_avg = ( prev_photocell[2] + prev_photocell[3] ) / 2
		old_avg = ( prev_photocell[0] + prev_photocell[1] ) / 2

		if ( prev_photocell[0] != -1
				and prev_photocell[2] < PHOTOCELL_LIGHT and prev_photocell[3] < PHOTOCELL_LIGHT
				and new_avg < ( old_avg - PHOTOCELL_DIFF ) ) :
			print 'Photocell: {0}'.format( prev_photocell )
			return True

	return False

def is_ultrasonic_triggered() :
	global prev_ultrasonic

	# Take 6 readings
	for i in range( 1, 4 ):
		ultrasonic = read_ultrasonic()
		#Shift readings
		prev_ultrasonic = ( prev_ultrasonic[1], prev_ultrasonic[2], prev_ultrasonic[3], ultrasonic )

		if ( is_light_enough()
				and prev_ultrasonic[0] != -1
				and prev_ultrasonic[2] < ULTRASONIC_DIST and prev_ultrasonic[3] < ULTRASONIC_DIST
				and prev_ultrasonic[0] > ULTRASONIC_DIST and prev_ultrasonic[1] > ULTRASONIC_DIST ) :
			print 'Ultrasonic: {0}'.format( prev_ultrasonic )
			return True

	return False

def reset_prev_readings() :
	global prev_photocell, prev_ultrasonic, prev_button

	prev_button = GPIO.HIGH
	prev_photocell = ( -1, -1, -1, -1 )
	prev_ultrasonic = ( -1, -1, -1, -1 )
	time.sleep( 1 )

# Get the sensor variables and timer ready
reset_prev_readings()
time.clock()

try :
	while ( True ) :
		if ( is_button_triggered() ) :
			take_picture( BUTTON_LED_PIN, 'Button' )
		elif ( is_photocell_triggered() ) :
			take_picture( PHOTOCELL_LED_PIN, 'Photocell' )
		elif ( is_ultrasonic_triggered() ) :
			take_picture( ULTRASONIC_LED_PIN, 'Ultrasonic' )
except KeyboardInterrupt :
	print 'Exiting via CTRL+C...'
finally :
	GPIO.cleanup()
