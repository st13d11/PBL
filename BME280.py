#coding: utf-8

from smbus2 import SMBus
import time

bus_number = 1
i2c_address = 0x77

bus = SMBus(bus_number)

digT = []
digH = []

t_fine = 0.0

def readData():
    data = []
    for i in range (0xF7, 0xF7+8):
        data.append(bus.read_byte_data(i2c_address, i))
    temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    hum_raw = (data[6] << 8) | data[7]
    
    T = compensate_T(temp_raw)
    H = compensate_H(hum_raw)
    
    index = 0.81 * T + 0.01 * H * (0.99 * T - 14.3) + 46.3
    
    return T + "," + H + "," + index

def compensate_T(adc_T):
    global t_fine
    v1 = (adc_T / 16384.0 - digT[0] / 1024.0) * digT[1]
    v2 = (adc_T / 131072.0 - digT[0] / 8192.0) * (adc_T / 131072.0 - digT[0] / 8192.0) * digT[2]
    t_fine = v1 + v2
    temperature = t_fine / 5120.0
    
    return "%.2f" % (temperture)

def compensate_H(adc_H)
    global t_fine
    var_h = t_fine - 76800.0
    if var_h != 0:
        var_h = (adc_H - (digH[3] * 64.0 + digH[4]/16384.0 * var_h)) * (digH[1] / 65536.0 * (1.0 + digH[5] / 67108864.0 * var_h * (1.0 + digH[2] / 67108864.0 * var_h)))
    else:
        return 0
    var_h = var_h * (1.0 - digH[0] * var_h / 524288.0)
    if var_h > 100.0
        var_h = 100.0
    elif var_h < 0.0
        var_h = 0.0
    return "%.2f" % (var_h)
