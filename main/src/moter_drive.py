# time: 2024/10/15
# author: zxy  

'''
    >>> 树莓派小车电机驱动程序
    使用时参照run函数，先实例化一个car类，然后初始化pwm并启动
    修改car类中的forward、backward、left、right、stop函数实现小车的动作
    使用pwm.ChangeDutyCycle()函数实现电机的速度控制
'''

import RPi.GPIO as gpio
import time

# 定义引脚
pin1 = 12  # -> IN1
pin2 = 16  # -> IN2
pin3 = 18  # -> IN3
pin4 = 22  # -> IN4
ENA = 38   # -> ENA PWM
ENB = 40   # -> ENB PWM

gpio.setwarnings(False)
# 设置gpio口为BOARD编号规范
gpio.setmode(gpio.BOARD)

# car类实现小车轮子驱动
class CarMoter(object):
    def __init__(self, pins: list):
        # 传入参数为一个数组，分别代表四个电机接口的GPIO口号，电机使能接口的GPIO口号
        if len(pins) < 6:
            raise ValueError("请提供至少6个GPIO接口的引脚号")
        
        self.pin1, self.pin2, self.pin3, self.pin4, self.ENA, self.ENB = pins[:6]

        gpio.setup(self.pin1, gpio.OUT)
        gpio.setup(self.pin2, gpio.OUT)
        gpio.setup(self.pin3, gpio.OUT)
        gpio.setup(self.pin4, gpio.OUT)
        gpio.setup(self.ENA, gpio.OUT)
        gpio.setup(self.ENB, gpio.OUT)

        self.pwm1 = gpio.PWM(self.ENA, 50)# 左侧电机pwwm波
        self.pwm2 = gpio.PWM(self.ENB, 50)# 右侧电机pwm波
        self.pwm1.start(0)
        self.pwm2.start(0)
    
    # moter_speed control
    '''
        @brief: set motor speed
        @param speed_left: left motor speed
        @param speed_right: right motor speed
        @return: None
    '''
    def set_speed(self, speed_left: int, speed_right: int):
        if speed_left < 0 or speed_left > 100 or speed_right < 0 or speed_right > 100:
            raise ValueError("duty cycle should be between 0 and 100")
        self.pwm1.ChangeDutyCycle(speed_left)
        self.pwm2.ChangeDutyCycle(speed_right)

    # moter_action control
    '''
        @brief: set motor action
        @param action: action name
        @return: None
    '''
    
    def forward(self):
        gpio.output(self.pin1, gpio.HIGH)  # 将pin1接口设置为高电压
        gpio.output(self.pin2, gpio.LOW)  # 将pin2接口设置为低电压
        gpio.output(self.pin3, gpio.HIGH)  # 将pin3接口设置为高电压
        gpio.output(self.pin4, gpio.LOW)  # 将pin4接口设置为低电压
        print("forward")

    def backward(self):
        gpio.output(self.pin1, gpio.LOW)
        gpio.output(self.pin2, gpio.HIGH)
        gpio.output(self.pin3, gpio.LOW)
        gpio.output(self.pin4, gpio.HIGH)
        print("backward")

    def left(self):
        gpio.output(self.pin1, gpio.LOW)
        gpio.output(self.pin2, gpio.HIGH)
        gpio.output(self.pin3, gpio.HIGH)
        gpio.output(self.pin4, gpio.LOW)
        print("left")

    def right(self):
        gpio.output(self.pin1, gpio.HIGH)
        gpio.output(self.pin2, gpio.LOW)
        gpio.output(self.pin3, gpio.LOW)
        gpio.output(self.pin4, gpio.HIGH)
        print("right")

    def stop(self):
        gpio.output(self.pin1, gpio.LOW)
        gpio.output(self.pin2, gpio.LOW)
        gpio.output(self.pin3, gpio.LOW)
        gpio.output(self.pin4, gpio.LOW)
        print("stop")


def run():

    car = CarMoter(pins=[pin1,pin2,pin3,pin4,ENA,ENB])
    car.forward()
    print("GO!")

    # 让小车每秒钟逐渐增加速度
    for i in range(6):
        car.pwm1.ChangeDutyCycle(10 * i)
        car.pwm2.ChangeDutyCycle(10 * i)
        time.sleep(0.2)
        print(i,"'s speed up!")

    print("Over")
    # 让小车停止,释放资源
    gpio.cleanup()
    car.pwm1.stop()
    car.pwm2.stop()

if __name__ == "__main__":
    run()