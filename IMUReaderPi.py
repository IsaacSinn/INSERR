# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from datetime import datetime
import board
import adafruit_bno055


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_bno055.BNO055_I2C(i2c)

# If you are going to use UART uncomment these lines
# uart = board.UART()
# sensor = adafruit_bno055.BNO055_UART(uart)

last_val = 0xFFFF


def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result

localTime = time.strftime('%Y-%m-%d, %H-%M-%S')
timeObj = datetime.now()

file1 = open('./IMUData/IMU_Data ' + localTime + '.txt', 'w')
file1.write("Temp (c), Acc\n")

def write():
    while True:
        #print("Temperature: {} degrees C".format(sensor.temperature))
        
        # print(
        #     "Temperature: {} degrees C".format(temperature())
        # )  # Uncomment if using a Raspberry Pi
        
        # print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
        # print("Magnetometer (microteslas): {}".format(sensor.magnetic))
        # print("Gyroscope (rad/sec): {}".format(sensor.gyro))
        # print("Euler angle: {}".format(sensor.euler))
        # print("Quaternion: {}".format(sensor.quaternion))
        # print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
        # print("Gravity (m/s^2): {}".format(sensor.gravity))
        # print()
        
        file1.write("(" + str(temperature()) +")\t" + str(sensor.acceleration) + "\t" + str(sensor.magnetic) +"\t" + str(sensor.gyro)+ "\t" + str(sensor.euler)+"\t" + str(sensor.quaternion)+"\t" + str(sensor.linear_acceleration)+"\t" + str(sensor.gravity)+ "\t(" +  str(timeObj) +")\n")
        time.sleep(0.01)
