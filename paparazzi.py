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
PHOTOCELL_LIGHT  = 50
PHOTOCELL_DIFF   = 100
ULTRASONIC_NEAR  = 100
ULTRASONIC_FAR   = 120

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
	os.system( '/opt/bloginabox/biab camera-take-photo "' + datetime.now().strftime( '%-I:%M:%S %p' ) + ' - ' + title + '"' )
	GPIO.output( led_pin, GPIO.LOW )
	reset_prev_readings()

# https://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading
def read_photocell() :
	GPIO.setup( PHOTOCELL_PIN, GPIO.OUT )
	GPIO.output( PHOTOCELL_PIN, GPIO.LOW )
	time.sleep( 0.05 )

	start = time.time()
	GPIO.setup( PHOTOCELL_PIN, GPIO.IN )

	end = start
	while ( GPIO.input( PHOTOCELL_PIN ) == GPIO.LOW ) :
		end = time.time()

	return int( round( ( end - start ) * 1000 ) )

# https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
def read_ultrasonic() :
	# Trigger the sensor
	GPIO.output( ULTRASONIC_TRIG_PIN, GPIO.HIGH )
	time.sleep( 0.00001 )
	GPIO.output( ULTRASONIC_TRIG_PIN, GPIO.LOW )

	# Read the sensor
	while ( True ) :
		pulse_start = time.time()
		if ( GPIO.input( ULTRASONIC_ECHO_PIN ) == GPIO.HIGH ) :
			break
	while ( True ) :
		pulse_end = time.time()
		if ( GPIO.input( ULTRASONIC_ECHO_PIN ) == GPIO.LOW ) :
			break

	time.sleep( 0.0001 )

	return int( round( ( pulse_end - pulse_start ) * 17150 ) )

def is_button_triggered() :
	global prev_button
	button = GPIO.input( BUTTON_PIN )
	trigger = False == button and True == prev_button
	prev_button = button

	return trigger

def is_photocell_triggered() :
	global prev_photocell

	# Take 6 readings
	for i in range( 1, 6 ):
		photocell = read_photocell()
		# Shift readings
		prev_photocell = ( prev_photocell[1], prev_photocell[2], prev_photocell[3], prev_photocell[4], prev_photocell[5], photocell )

		if ( prev_photocell[0] != -1 ) :
			if ( prev_photocell[3] < PHOTOCELL_LIGHT and  prev_photocell[4] < PHOTOCELL_LIGHT and prev_photocell[5] < PHOTOCELL_LIGHT ) :
				new_avg = ( prev_photocell[3] + prev_photocell[4] + prev_photocell[5] ) / 3
				old_avg = ( prev_photocell[0] + prev_photocell[1] + prev_photocell[2] ) / 3
				if ( new_avg < ( old_avg - PHOTOCELL_DIFF ) ) :
					#print 'Photocell: {0}'.format( prev_photocell )
					return True

	return False

def is_ultrasonic_triggered() :
	global prev_ultrasonic

	# Take 6 readings
	for i in range( 1, 6 ):
		ultrasonic = read_ultrasonic()
		#Shift readings
		prev_ultrasonic = ( prev_ultrasonic[1], prev_ultrasonic[2], prev_ultrasonic[3], prev_ultrasonic[4], prev_ultrasonic[5], ultrasonic )

		if ( prev_ultrasonic[0] != -1 ) :
			if ( prev_ultrasonic[3] < ULTRASONIC_NEAR and prev_ultrasonic[4] < ULTRASONIC_NEAR and prev_ultrasonic[5] < ULTRASONIC_NEAR ) :
				if ( prev_ultrasonic[0] > ULTRASONIC_FAR and prev_ultrasonic[1] > ULTRASONIC_FAR and prev_ultrasonic[2] > ULTRASONIC_FAR ) :
					#print 'Ultrasonic: {0}'.format( prev_ultrasonic )
					return True

	return False

def reset_prev_readings() :
	global prev_photocell, prev_ultrasonic, prev_button
	prev_button = True
	prev_photocell = ( -1, -1, -1, -1, -1, -1 )
	prev_ultrasonic = ( -1, -1, -1, -1, -1, -1 )
	time.sleep( 1 )

reset_prev_readings()

while True:
	if ( is_button_triggered() ) :
		take_picture( BUTTON_LED_PIN, 'Button' )
	elif ( is_photocell_triggered() ) :
		take_picture( PHOTOCELL_LED_PIN, 'Photocell' )
	elif ( is_ultrasonic_triggered() ) :
		take_picture( ULTRASONIC_LED_PIN, 'Ultrasonic' )
