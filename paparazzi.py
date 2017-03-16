#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from datetime import datetime
import os

# GPIO Pins
BUTTON_PIN          = 23
BUTTON_LED_PIN      = 5
PHOTOCELL_PIN       = 18
PHOTOCELL_LED_PIN   = 6
ULTRASONIC_TRIG_PIN = 20
ULTRASONIC_ECHO_PIN = 21
ULTRASONIC_LED_PIN  = 13

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

	time = datetime.now().strftime( '%-I:%M:%S %p' )
	os.system( '/opt/bloginabox/biab camera-take-photo "' + time + ' - ' + title + '"' )

	GPIO.output( led_pin, GPIO.LOW )

# https://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading
def read_photocell() :
    reading = 0
    GPIO.setup( PHOTOCELL_PIN, GPIO.OUT )
    GPIO.output( PHOTOCELL_PIN, GPIO.LOW )
    time.sleep( 0.1 )

    GPIO.setup( PHOTOCELL_PIN, GPIO.IN )
    # This takes about 1 millisecond per loop cycle
    while ( GPIO.input( PHOTOCELL_PIN ) == GPIO.LOW ):
        reading += 1

    return reading

# https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
def read_ultrasonic() :
	# Trigger the sensor
	GPIO.output( ULTRASONIC_TRIG_PIN, GPIO.HIGH )
	time.sleep(0.00001)
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

	return round( ( pulse_end - pulse_start ) * 17150, 2 )

prev_button = True
prev_photocell = read_photocell()
prev_ultrasonic = read_ultrasonic()
time.sleep( 2 )

while True:
	button = GPIO.input( BUTTON_PIN )
	photocell = read_photocell()
	ultrasonic = read_ultrasonic()

	if ( False == button == False and True == prev_button ) :
		take_picture( BUTTON_LED_PIN, 'Button' )
	elif ( photocell != -1 and photocell < 3000 and photocell < ( prev_photocell - 500 ) ) :
		take_picture( PHOTOCELL_LED_PIN, 'Photocell' )
	elif ( ultrasonic != -1 and ultrasonic < 100 and prev_ultrasonic > 150 ) :
		take_picture( ULTRASONIC_LED_PIN, 'Ultrasonic' )

	prev_button = button
	prev_photocell = photocell
	prev_ultrasonic = ultrasonic
