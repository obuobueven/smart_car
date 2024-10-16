# infrared sensor driver

import RPi.GPIO as GPIO
import time

# set GPIO
pin_obstacle_left = 5
pin_obstacle_right = 6

pin_track_left = 13
pin_track_right = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class CarInfrared(object):
    def __init__(self, pins:list):
        # set pins for infrared sensor
        self.pin_obstacle_left = pins[0]
        self.pin_obstacle_right = pins[1]

        self.pin_track_left = pins[2]
        self.pin_track_right = pins[3]

        # set GPIO input mode
        GPIO.setup(self.pin_obstacle_left, GPIO.IN)
        GPIO.setup(self.pin_obstacle_right, GPIO.IN)

        GPIO.setup(self.pin_track_left, GPIO.IN)
        GPIO.setup(self.pin_track_right, GPIO.IN)

    def get_obstacle_status(self):
        # get the status of obstacle sensor
        status_obstacle_left = GPIO.input(self.pin_obstacle_left)
        status_obstacle_right = GPIO.input(self.pin_obstacle_right)

        # return the status of obstacle sensor
        return [status_obstacle_left, status_obstacle_right]
    
    def get_track_status(self):
        # get the status of track sensor
        status_track_left = GPIO.input(self.pin_track_left)
        status_track_right = GPIO.input(self.pin_track_right)

        # return the status of track sensor
        return [status_track_left, status_track_right]
    

if __name__ == '__main__':
    try:
        car = CarInfrared()
        while True:
            [left, right] = car.get_obstacle_status()
            # [l, r] = car.get_track()
            print("Obstacle Left: ", left, "Obstacle Right: ", right)
            time.sleep(1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("program stopped by User")
        GPIO.cleanup()