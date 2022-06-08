from gpiozero import Button

rain_sensor = Button(6)
count = 0

BUCKET_SIZE = 0.2794

def bucket_tipped():
    global count
    count += 1
    print(count * BUCKET_SIZE)

def reset_rain():
    global count
    count = 0 

# while True:
#     rain_sensor.when_pressed = bucket_tipped