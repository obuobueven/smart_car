# import RPi.GPIO as gpio
import time

class Car:
    def __init__(self, pins: list):
        # 传入参数为一个数组，分别代表四个电机接口的GPIO口号，电机使能接口的GPIO口号
        if len(pins) < 6:
            raise ValueError("请提供至少6个GPIO接口的引脚号")
        
        self.pin1, self.pin2, self.pin3, self.pin4, self.ENA, self.ENB = pins[:6]



    def forward(self):
        print("forward")

    def backward(self):
        print("backward")
    def left(self):
        print("left")

    def right(self):
        print("right")

    def stop(self):
        print("stop")


def run(flag):
    # 实例化一个Car对象
    car = Car(pins=[11, 13, 15, 16, 18, 22])
    if flag == 1:
        car.forward()
    elif flag == 2:
        car.backward()
    elif flag == 3:
        car.left()
    elif flag == 4:
        car.right()


# 调用main函数，传入相应的flag值
if __name__ == "__main__":
    run(flag = 3)  # 可以根据需要修改flag值进行测试
