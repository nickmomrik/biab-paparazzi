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
Update any of the necessary GPIO PIN values at the top of `paparazzi.py` and then either run manually `python paparazzy.pi` or [run as a service](http://www.diegoacuna.me/how-to-run-a-script-as-a-service-in-raspberry-pi-raspbian-jessie/). Depending on your envionment, you may need to update the TEST CONSTANT values so that triggers don't happen too often.
