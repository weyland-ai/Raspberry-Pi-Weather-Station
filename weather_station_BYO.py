from gpiozero import Button
import time
import math
import bme280_sensor
import wind_direction_BYO
import statistics
import ds18b20_therm

wind_count = 0    # Counts how many half-rotations
radius_cm = 9.0   # Radius of your anemometer
wind_interval = 5 # How often (secs) to sample speed
interval =  5     # measurements recorded every 5 seconds
CM_IN_A_KM = 100000.0 # 1 Kilometer = 100000 centimeters
SECS_IN_AN_HOUR = 3600
ADJUSTMENT = 1.18
BUCKET_SIZE = 0.2794 # 0.2794 mm of weight while tip the bucket
rain_count = 0 # How many time the rain bucket tips
gust = 0
store_speeds = []
store_directions = []

# Every half-rotation, add 1 to count
def spin():
    global wind_count
    wind_count += 1
    #print( wind_count )

# Using the formual: speed = distance / time
"""
In order to find the distance, we need to multiply the rotation by circumference  --> speed = (rotation * circumference) / time
In order to find the circumference, we use the formula C = 2 * pi * radious
Signals must be divided by 2 becasue a whole rotation causes two singlas ---> speed = ((signals / 2) * (2 * pi * radious)) / time
Using the Oracle Weather Station, we are told the radious is 9.0 cm

Given this information we can proform a sample calculation.  Lets say anemometer signaled 20 time in a 5 second period:

speed = ((20 / 2) * (2 * pi * 9.0)) / 5
Therefore:

speed = 113 cm/s

However, it would be more practicle to use km/h:

See code below...

"""

def calculate_speed(time_sec):
    global wind_count
    global gust

    # calculating circumference
    circumference_cm = (2 * math.pi) * radius_cm 

    # Number of rotations
    rotations = wind_count / 2.0

    # Calculate distance travelled by a cup in km
    # Distance = (circumference * rotation) / time (converting CM to KM --> CM_IN_A_KM)
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM 

    # Speed = distance / time
    # Speed in seconds
    km_per_sec = dist_km / time_sec

    # Converting Speed in seconds to hours
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR

    # Calculate speed
    final_speed = km_per_hour * ADJUSTMENT

    return final_speed

# Number of times rain bucket has tipped
def bucket_tipped():
    global rain_count
    rain_count = rain_count + 1
    #print (rain_count * BUCKET_SIZE)

# Setting rain bucket back to zero
def reset_rainfall():
    global rain_count
    rain_count = 0

# Setting wind_count back to zero
def reset_wind():
    global wind_count
    wind_count = 0

# Setting gust back to zero
def reset_gust():
    global gust
    gust = 0

wind_speed_sensor = Button(5)
wind_speed_sensor.when_activated = spin
temp_probe = ds18b20_therm.DS18B20()

rain_sensor = Button(6)
rain_sensor.when_pressed = bucket_tipped

while True:
    # time.time() is measured in Unix epoch time. ex: 1654796583.301785 = 2022-6-9-5:46:20
    start_time = time.time()
    # As long as when the time started minus the current time is less than or equal to 5 seconds (interval)
    while time.time() - start_time <= interval:
        # set wind_start_time = to current time...
        wind_start_time = time.time()
        # Than set wind_count to zero
        reset_wind() 
        # while current time minues when the wind started is less than 5 (wind_interval)
        while time.time() - wind_start_time <= wind_interval:
            # Store the value from get_get() into store_directions list
            store_directions.append(wind_direction_BYO.get_value())

        # storing wind_speed in final_speed, then adding it to store_speeds list
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
        
    wind_average = wind_direction_BYO.get_average(store_directions)
    # getting hight value from store_speeds and storing it in wind_gust
    wind_gust = max(store_speeds) # max function returns the item with the hightest value
    wind_speed = statistics.mean(store_speeds) # getting the mean value from store_speeds and setting it to wind_speed
    rainfall = rain_count * BUCKET_SIZE
    reset_rainfall()
    store_speeds = []
    store_directions = []
    ground_temp = temp_probe.read_temp() # getting data from ds18b thermostat and setting it to ground_temp
    humidity, pressure, ambient_temp = bme280_sensor.read_all() # getting data from bme280 sensor with read_all() function and setting the data to three variables

                      # Round to the nearest decimal
    print('Wind Dir:',round(wind_average,1), 'Wind Speed:',round(wind_speed,1), 'Wind Gust:',round(wind_gust,1), 'Rainfall:',round(rainfall,1),'Humidity:',round(humidity,1),'Pressure:', round(pressure,1), 'Ambient Temp:',round(ambient_temp,1),'Ground Temp:', round(ground_temp,1))


"""
UNDERSTANDING HOW THE 3 WHILE LOOPS WORK...

import time
import math

while True:
    start_time = time.time()
    print('start_time ' + str(start_time))
    while time.time() - start_time <= 5: # while keeps looking at current time, subtracting it with start_time, and checking it aginst 5
        wind_start_time = time.time()
        print('wind_start_time: ' + str(wind_start_time))
        print(math.trunc(time.time() - wind_start_time))
        while time.time() - wind_start_time <= 5:
            print(math.trunc(time.time() - wind_start_time))
            time.sleep(1)

"""


