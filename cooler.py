import RPi.GPIO as GPIO
import sys, traceback

from subprocess import check_output
from re import findall
from time import sleep

def get_temperature():
    temperature = check_output(["vcgencmd", "measure_temp"]).decode()
    temperature = float(findall("\d+\.\d+", temperature)[0])
    return(temperature)

try:
    temperatureOn = 59
    temperatureOff = 40
    temperatureClearance = temperatureOn - temperatureOff
    
    controlPin = 14
    pinState = False
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(controlPin, GPIO.OUT, initial=0)
    
    while True:
        temperature = get_temperature()
        
        if temperature > temperatureOn and not pinState or temperature < temperatureOn - temperatureClearance and pinState:
            pinState = not pinState
            GPIO.output(controlPin, pinState)
            
        print(str(temperature) + " " + str(pinState))
        sleep(1)

except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")
except:
    print("Other Exception")
finally:
    print("Cleanup")
    GPIO.cleanup
    print(" End of program")