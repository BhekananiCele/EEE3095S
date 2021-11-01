import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from Client import *

# some global variables that need to change as we run the program
frequencyOfReadingData = 10.0
startTime = None

# DEFINE THE PINS USED HERE
btn_submit = 23

# Fuction to setup the GPIO Pins 
def setup():  
    #Button Setup
    GPIO.setup(btn_submit, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setup debouncing and callbacks
    GPIO.add_event_detect(btn_submit, GPIO.FALLING, callback=incrementFrequency, bouncetime=300)
 
# Function to increase the sampling time
def incrementFrequency(channel):
    global frequencyOfReadingData
    if (frequencyOfReadingData ==10.0):
        frequencyOfReadingData = 1.0
    elif (frequencyOfReadingData ==1.0):
        frequencyOfReadingData = 5.0
    else:
        frequencyOfReadingData = 10.0

# Function to get sensor_values from the ADC
def fetch_sensor_vals(channel):
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    
    if(channel == 1):
         # create an analog input channel on pin 1
        chan1 = AnalogIn(mcp, MCP.P1)    
        return chan1.value, chan1.voltage
    
    elif(channel == 2):
        # create an analog input channel on pin 2
        chan2 = AnalogIn(mcp, MCP.P2)
        return chan2.value, chan2.voltage
    
# Function to calculate temperature from
# ADC value, rounded to specified
# number of decimal places.
def convertToTemp(tempArg, places=2):
    temp = ((tempArg)/float(1023))
    temp = round(temp * (1/0.01),places)
    return temp

# Fuction, it uses threads to read data from the sensors
def main():
    global startTime
    runTime = (datetime.now() - startTime).total_seconds() # Calculates run time
    global frequencyOfReadingData
    tempADC_Value, tempVoltage = fetch_sensor_vals(1)
    lightADC_Value, lightVolatge = fetch_sensor_vals(2)
    
    sendDataToServer(str(tempADC_Value) +" "+ str(lightADC_Value))
    #print("{:<11d}{:<16d}{:05.2f} C{:>10d}".format(int(runTime), tempADC_Value, convertToTemp(tempADC_Value,2), lightADC_Value))
    
    thread = threading.Timer(frequencyOfReadingData, main)
    thread.daemon = True  # Daemon threads exit when the program does
    thread.start()
    
# Fuction, to print the heading of the table       
def printHeading():
    print('{:<11s}{:<16s}{:<13s}{:<17s}'.format("Runtime", "Temp Reading", "Temp", "Light Reading"))
    
if __name__ == "__main__":
    try:
        print("Client Running")
        
        thread = threading.Thread(target=ListenToServer)
        thread.daemon = True
        thread.start()
        
        setup()
        #printHeading()
        startTime = datetime.now()
        main()
                
        while True:
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()