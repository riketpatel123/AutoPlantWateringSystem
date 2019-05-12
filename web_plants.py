from flask import Flask, render_template, redirect, url_for #this import is used in some of the functions below to return the value
import psutil #this import is used in auto_water function for retrieving information on running processes
import datetime #this import is used in template function for getting current date and time on system
import water #importing the water.py file in some of the functions to call the methods
import os #This import is used in auto_water for running operating systems cmd commands

app = Flask(__name__)

#Author: Riket Patel
#Function Name: template
#Parameters: 3 - title, text , event - title of the main page , status text, to show the last watered event
#Date: March 14, 2019
#Returns: templateDate
def template(title = "Raspberry Pi Auto Planting!", text = "",event = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text,
        'event': event
        }
    return templateDate

#Author: Riket Patel
#Function Name: home
#Parameters:  0
#Date: March 14, 2019
#Returns: render_template (main.html)
@app.route("/")
def home():
    templateData = template()
    return render_template('main.html', **templateData)

#Author:RiketS Patel
#Function Name: check_last_watered
#Parameters:  0
#Date: March 14, 2019
#Returns: render_template (main.html)
@app.route("/last_watered")
def check_last_watered():
    templateData = template(event = water.get_last_watered())
    return render_template('main.html', **templateData)

#Author: Riket Patel
#Function Name: check_sensor_status
#Parameters:  0
#Date: March 14, 2019
#Returns: render_template (main.html)
@app.route("/sensor")
def check_sensor_status():
    status = water.get_status()
    message = ""
    if (status == 1):
        message = "Water Moisture level is Low. Please Water!"
    else:
        message = "Water Moisture level is Perfect!"

    templateData = template(text = message)
    return render_template('main.html', **templateData)


#Author: Riket Patel
#Function Name: watered_once
#Parameters:  0
#Date: March 18, 2019
#Returns: render_template (main.html)
@app.route("/water")
def watered_once():
    water.pump_on()
    templateData = template(text = "Watered Once",event= water.last_time_watered)
    return render_template('main.html', **templateData)

#Author: Riket Patel
#Function Name: auto_water
#Parameters:  1 - toggle (user input)
#Date: March 18, 2019
#Returns: render_template (main.html)
@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Auto Watering Service On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python3 auto_water.py&")
    else:
        templateData = template(text = "Auto Watering Service Off")
        os.system("pkill -f water.py")

    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
