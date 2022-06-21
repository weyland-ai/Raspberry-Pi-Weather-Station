import bme280 # Provides a library for reading and interpreting Bosch BME280 environmental sensor data.  Reads temperature, humidity, and pressure.
import smbus2 # used to interact with bme280 sensor
# from time import sleep --> only necessary when working with single file

port = 1 # 1 is part of the i2c file name: i2c-1.  If port is anything other than 1, an error will show saying: No such file: '/dev/i2c-2'   if port was = to 2
address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

def read_all():
    bme280_data = bme280.sample(bus,address)
    return bme280_data.humidity, bme280_data.pressure, bme280_data.temperature
    
# while True:
#     bme280_data = bme280.sample(bus,address)
#     humidity = bme280_data.humidity
#     pressure = bme280_data.pressure
#     ambient_temperature = bme280_data.temperature
#     print(humidity, pressure, ambient_temperature)
#     sleep(1)
