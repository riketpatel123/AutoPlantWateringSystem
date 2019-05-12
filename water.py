import RPi.GPIO as GPIO #this import GPIO statment help the program to read board pins
import datetime # this import statment give date and time format to our system.
import time #this import statment return current time to our system

init = False
last_time_watered= "Never"

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

#Auther: Riket Patel
#Function Name: get_last_watered
#parameters: 0
#Date: March 18, 2019
#Returns: single line text
def get_last_watered():
    if last_time_watered:
        return last_time_watered
    else:
        return "NEVER!"

#Author: From Instructables.com https://www.instructables.com/id/Soil-Moisture-Sensor-Raspberry-Pi/
#Function: get_status
#parameters: 1 - pin, GPIO raspberry pin no. 8
#Date: March 22, 2019
def get_status(pin = 8):
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)

#Author: Riket Patel
#Function:setup_pin
#parameter: 1 - pin, raspberry pi GPIO pin
#Date: April 1, 2019
def setup_pin(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)

#Author:Riket Patel
#Function:pump_on
#Parameter: 3 - GPIO pin for pump, delay time for pump
#Date: April 2, 2019
#Code Reference :Author:- Misty Lackie (https://github.com/mistylackie/solar-water-bot/blob/master/SoilSensor.py)
def pump_on(pump_pin = 7, delay = 1):
    setup_pin(pump_pin)
    date_time = datetime.datetime.now()

    global last_time_watered
    last_time_watered = "Plant Watered at: {}".format(date_time.strftime("%Y-%m-%d %H:%M:%S"))

    #Function to run the pump. Reference code GitHub: https://github.com/mistylackie/solar-water-bot/blob/master/SoilSensor.py
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(2)
    GPIO.output(pump_pin, GPIO.HIGH)

#Author:Riket Patel
#Function:auto_water
#Parameter: 3 - GPIO pin of pump, GPIO pin of soil moisture sensor, delay time for pump to on
#Date: April 1, 2019
def auto_water(pump_pin = 7, sensor_pin = 8,delay_time = 5):

    setup_pin(pump_pin)

    water_count= 0

    print("auto water plant is activated! Press CTRL+C to exit")
    try:
        while 1 and water_count < 10:
            time.sleep(delay_time)
            soil_status_wet = get_status(pin = sensor_pin) == 0
            if not soil_status_wet:
                if water_count < 5:
                    pump_on(pump_pin, 1)
                water_count += 1
            else:
                water_count = 0
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI
        print("CTRL+C Keyboard Interrupted")
