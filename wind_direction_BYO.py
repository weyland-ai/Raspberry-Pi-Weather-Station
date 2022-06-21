from gpiozero import MCP3002
import time
import math

adc = MCP3002(channel=0) # read channel zero from the ADC
count = 0
values = []

# List of possible correct values to check against ADC
# using the voltage_divider, and looping through resistances, we can find the volts and angle of the vane:

# def voltage_divider(r1, r2, vin):
#    vout = (vin * r1) / (r1 + r2)
#    return round(vout, 3)

# voltage_divider(4700, resistances[resistance], 3.3)

       # volts, angle
volts = {0.4: 0.0, 
         1.4: 22.5,
         1.2: 45.0,
         2.8: 67.5,
         2.7: 90.0,
         2.9: 112.5,
         2.2: 135.0,
         2.3: 135.0,
         2.5: 157.5,
         1.8: 180.0,
         2.0: 202.5,
         0.7: 225.0,
         0.8: 247.5,
         0.1: 270.0,
         0.3: 292.5,
         0.2: 315.0,
         0.6: 337.5}

#while True:
#    wind =round(adc.value*3.3,1)
#    if not wind in volts:
#        print('unknown value ' + str(wind) + ' ' + str(volts[wind]))
#    else:
#        print('found ' + str(wind) + ' ' + str(volts[wind]))


def get_average(angles):
    if len(angles)==0:
        return 0.0
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    
    s = sin_sum / flen
    c = cos_sum / flen
    arc = math.degrees(math.atan(s / c))
    average = 0.0

    if s > 0 and c > 0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360

    return 0.0 if average == 360 else average


def get_value(length=5):
    data = []
    #print("Measuring wind direction for %d seconds..." % length)
    start_time = time.time() 

    while time.time() - start_time <= length: # While it has been less than or equal to 5 seconds 
        direction = round(adc.value*3.3,1) # analog voltage = adc.value * (3.3 volts) reference voltage supplied to the ADC. 1 is to round to the nearest decimal
        if not direction in volts: # keep only good measurements. If the direction of the Wind vane is not in voltes, print unknow direction
            print('unknown value ' + str(direction))
            pass
        else:
            data.append(volts[direction]) # if wind vane direction is in volts, add it to data list 

    return get_average(data)



