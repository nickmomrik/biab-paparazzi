# Blog in a Box Paparazzi
Let [Blog in a Box](https://inabox.blog) take pictures based on sensors or actions.

## Parts
 * [Photocell](https://www.adafruit.com/products/161)
 * [Ultrasonic Sensor - HC-SR04](https://www.sparkfun.com/products/13959)
 * [Tactile button](https://www.adafruit.com/products/367)
 * [10mm LED](https://www.adafruit.com/products/845)
 * 1uF capacitor
 * Various resistors

## Wiring
Check out the [Fritzing](./paparazzi.fzz) or reference the screenshot below.

![Blog in a Box Paparazzi Fritzing](./paparazzi-fritzing.png?raw=true "Blog in a Box Paparazzi Fritzing")

## Instructions
There are 2 versions:
 * `paparazzi.py` - A lot of code to control the sensors and hack all you want
 * `paparazzi-gpiozero.py` - uses [gpiozero](https://gpiozero.readthedocs.io/en/stable/) to handle all of the heavy lifting

If you use the gpiozero version you'll need to install the library...
`sudo apt-get update`
`sudo apt-get install python3-gpiozero`
OR (depending if you run Python 2 or 3)
`sudo apt-get install python-gpiozero`

For both versions you'll want to update the GPIO PIN values at the top of the file to match your wiring. You may also need to adjust the TEST CONSTANT values. Then either run the program manually `python paparazzy[-gpiozero].py` or [run as a service](http://www.diegoacuna.me/how-to-run-a-script-as-a-service-in-raspberry-pi-raspbian-jessie/).
