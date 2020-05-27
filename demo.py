#coding=utf-8
import os

dir = os.path.join(os.getcwd(),"static/imgs/carpics")
print(dir)

from check_car import car_check

result = car_check(dir+"123.jpg")
print(result)
