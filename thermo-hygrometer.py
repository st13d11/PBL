#coding: utf-8

import BME280
import datetime.datetime
import os
import RPi.GPIO as GPIO
import time

dir_path = '/home/hoge'
MD = 'MeasurementData.csv'
MDnoon = 'MeasurementData_Noon.csv'

dt = datetime.now()
if dt.strftime('%H') == 12 :
    flag = 1
now = dt.strftime('%Y/%m/%d/%H:%M')
data = BME280.readData()

GPIO.setmode(GPIO.BCM)
LED_R = 16
LED_B = 18

GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_R, GPIO.IN)
if 1 : #データチェック
    GPIO.output(LED_B, 1)
    time.sleep(1)
    GPIO.output(LED_B, 0)
    
    data.split(",")
    T = data[0]
    H = data[1]
    index = 0.81 * T + 0.01 * H * (0.99 * T - 14.3) + 46.3
    if index > 77 :
        GPIO.output(LED_R, 1)
        time.sleep(1)
        GPIO.output(LED_R, 0)
else :
    T = 'error'
    H = 'error'
    index = 'error'

csv = '{0},{1},{2},{3:.0d}'.format(now, T, H, index)

if not os.path.exists(dir_path) :
    os.mkdir(dir_path)
f = open(dir_path + "/" + MD, "a")
f.write(csv + '\n')
f.close

if flag :
    f = open(dir_path + "/" + MDnoon, "a")
    f.write(csv + '\n')
    f.close

GPIO.cleanup()
