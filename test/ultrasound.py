# ultrasound.py is a module for ultrasound sensor.

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

trig = 17
echo = 27
class CarUltrasound(object):
    def __init__(self,pins:list):
        # set pins for ultrasound sensor
        self.trig,self.echo = pins[:2]
        # set GPIO mode
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)

        # set initial distance
        self.last_distance = 0

    def get_distance(self):
        # set trigger to HIGH
        # faster than 10us
        GPIO.output(self.trig, False) 
        time.sleep(0.000002)
        GPIO.output(self.trig, True)  # emit ultrasonic pulse
        time.sleep(0.00001)                   # last 10us
        GPIO.output(self.trig, False) # end the pulse

        ii = 0
        # wait for echo to become HIGH
        while GPIO.input(self.echo) == 0:  # when receiving the echo, ECHO will become 1
            ii = ii + 1
            if ii > 10000: 
                print('Ultrasound error: the sensor missed the echo')
                return 0
            pass

        # record the time when the echo becomes HIGH
        start_time = time.time()
        # wait for echo to become LOW
        while GPIO.input(self.GPIO_ECHO) == 1:  # the duration of high level of ECHO is the time between the emitting the pulse and receiving the echo
                pass
        # record the time when the echo becomes LOW
        stop_time = time.time()
        # calculate the distance using the time difference
        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2

        return distance
    
    # 滑动平均滤波
    def distance_average(self):
        dist_current = self.get_distance()
        if dist_current == 0:  # if the sensor missed the echo, the output dis_mov_ave will equal the last dis_mov_ave
            return self.last_distance
        else:
            self.last_distance = 0.8*dist_current + 0.2*self.last_distance  # using the moving average of distance measured by sensor to reduce the error
            return self.last_distance
        

if __name__ == '__main__':
    try:
        car = CarUltrasound()
        while True:
            dist = car.get_distance()
            print("Measured Distance = {:.2f} cm".format(dist))
            time.sleep(1)
  
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()