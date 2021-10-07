
# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import datetime
import time
import decimal

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
pwm_led = None
trans_pin = None
guessed_number = 0
startTIme = None
value = None

# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = None
transistor = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n>>")
    print(option)
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    pass


# Setup Pins
def setup():
    global pwm_led
    global trans_pin
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
    # Setup regular GPIO
    #LEDS Setup
    for pinNo in LED_value:
        GPIO.setup(pinNo, GPIO.OUT)
    GPIO.setup(LED_accuracy, GPIO.OUT)

    for pinNo in LED_value:
        GPIO.output(pinNo, 0)
    GPIO.output(LED_accuracy, 0)
    
    #Button Setup
    GPIO.setup(btn_submit, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_increase, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    #Transistor Setup
    GPIO.setup(transistor, GPIO.OUT)
    GPIO.output(transistor, 0)
    
    
    # Setup PWM channels
    pwm_led = GPIO.PWM(LED_accuracy, 1000)
    trans_pin = GPIO.PWM(transistor, 2000)
    
    # Setup debouncing and callbacks
    GPIO.add_event_detect(btn_submit, GPIO.FALLING, callback=getStartTime, bouncetime=300)
    GPIO.add_event_detect(btn_submit, GPIO.RISING, callback=btn_guess_pressed, bouncetime=300)
    GPIO.add_event_detect(btn_increase, GPIO.FALLING, callback=btn_increase_pressed, bouncetime=300)




def getStartTime():
    global startTime
    startTIme = datetime.datetime.now()
# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = None
    # Get the scores
    
    # convert the codes back to ascii
    
    # return back the results
    return score_count, scores



# Save high scores
def save_scores():
    # fetch scores
    # include new score
    # sort
    # update total amount of scores
    # write new scores
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)

def toBinary(decimal):
    binary = []
    for bit in bin(decimal).replace("0b", "").zfill(3):
        binary.append(eval(bit))
    return binary

# Increase button pressed
def btn_increase_pressed(channel):
    global guessed_number
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess  
    if(guessed_number >= 7):
        guessed_number =0    
    guessed_number +=1
    LEDOutPut = toBinary(guessed_number)
    GPIO.output(LED_value[0],LEDOutPut[0])
    GPIO.output(LED_value[1],LEDOutPut[1])
    GPIO.output(LED_value[2],LEDOutPut[2])
    

# Guess button
def btn_guess_pressed(channel):
    global value
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    endDT = datetime.datetime.now()
    if(decimal.Decimal((endDT-startTIme).seconds)>2):
        end_of_game = True;
    else:
         # Compare the actual value with the user value displayed on the LEDs
        if(value == guessed_number):
             # if it's an exact guess:
            # - Disable LEDs and Buzzer
            GPIO.output(LED_value[0],0)
            GPIO.output(LED_value[1],0)
            GPIO.output(LED_value[2],0)            
            trans_pin.stop()
            # - tell the user and prompt them for a name            
        else:
            # Change the PWM LED
            # if it's close enough, adjust the buzzer            
            accuracy_leds()
            trigger_buzzer()
              
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count

# LED Brightness
def accuracy_leds():
    
    if(generate_number<=value):
        pwm_led.start((generate_number/value)*100)
    elif(generate_number>value):
        pwm_led.start(((8-generate_number)/(8-value))*100)
                      
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    pass

# Sound Buzzer
def trigger_buzzer():
    
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    trans_pin.start(1000)
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    if(abs(generate_number-value) == 3):
        trans_pin.ChangeFrequency(2000)
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    elif(abs(generate_number-value) == 2):
        trans_pin.ChangeFrequency(4000)
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    elif(abs(generate_number-value) == 1):
        trans_pin.ChangeFrequency(8000)        



if __name__ == "__main__":

        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass

        print(e)

        GPIO.cleanup()
