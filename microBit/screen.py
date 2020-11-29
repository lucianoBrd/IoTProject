# Import libraries
##################################################
from microbit import *
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from security import *
import radio
import random
##################################################

# Global variables
##################################################
# Network request
init = "chlib_request"
accept = "chlib_accept"
stop = "chlib_stop"
# Default communication addresse
default_address = "0x12345678"
# Default key for cipher
key = default_address 
# Initialize screen
initialize(pinReset=pin0)
clear_oled()
# Communication not established by default
com_established = False
##################################################

# Network functions 
##################################################
# Send message by radio to another micro:bit
# Encrypt the message before to send
def send_msg(message):
    q = vign(message, key, 'e')
    radio.send(q) # max size 251 bytes (octets)

# Receive message from another micro:bit by radio
# Decrypt the message before to return
def listen():
    q = radio.receive()
    m = vign(q, key, 'd')
    return m

# Protocols to initialize a connection or stop it
def manage_protocol(sig, com_established):
    if sig != None:
        # Messages are formated like this :
        # "request:addresse"
        # So we split the message in order to know wich request is it
        sig = sig.split(":")
        
        if sig[0] == init:
            # Initialize a connection with another micro:bit
            add = ""
            
            # Compute a new random addresse in order to use it for radio communications
            for i in range(0,8) :
                add += str(random.randint(0, 9))
                
            # Send accept request with the new addresse
            send_msg(accept+":0x"+add)
            return com_established
        
        elif sig[0] == accept:
            # Accept connection with another micro:bit
            # Get the new addresse
            add = int(sig[1])
            # Set the key for cipher with the new addresse
            key = str(add)

            # Send accept request with the new addresse
            # In order that the micro:bit who initialize
            # The communication change his addresse too
            if com_established == False:
                send_msg(accept+":"+str(add))

            # Change the addresse and set
            # That the communication is established
            radio.config(address=add)
            com_established = True
            display.scroll("INIT")
            return com_established
        
        elif sig[0] == stop and com_established:
            # Stop the connection with another micro:bit
            # Set default addresse, key 
            radio.config(address=int(default_address))
            key = default_address
            com_established = False
            display.scroll("STOP")
            return com_established
        
    return com_established
##################################################

# Config the radio
##################################################
radio.config(address=int(default_address))
radio.on()
##################################################

# Main prog
##################################################
while True:
    # Listen if another micro:bit want to initialize a communication
    if com_established == False:
        init_message = listen()
        com_established = manage_protocol(init_message, com_established)
    
    if com_established:
        # Check if we receive a message
        message = listen()
        if message != None:
            # Just want to have two char
            message = message[0:2]
            display.scroll(message)
            
            if (message == "LT"):
                # LT case
                # Display on screen lum then temp
                clear_oled()
                add_text(0, 0, "L: " + str(display.read_light_level()))
                add_text(0, 1, "T: " + str(temperature()))
                
                # JSON response, exemple:
                # {"l": "0", "t": "28", "o": "LT"}
                messageReturn = "{\"l\":\""+str(display.read_light_level())+"\",\"t\":\""+str(temperature())+"\",\"o\":\""+message+"\"}"
                
            elif (message == "TL"):
                # TL case
                # Display on screen temp then lum
                clear_oled()
                add_text(0, 0, "T: " + str(temperature()))
                add_text(0, 1, "L: " + str(display.read_light_level()))

                # JSON response, exemple:
                # {"t": "28", "l": "0", "o": "TL"}
                messageReturn = "{\"t\":\""+str(temperature())+"\",\"l\":\""+str(display.read_light_level())+"\",\"o\":\""+message+"\"}"
                
            else:
                # Error case
                # Display error on screen
                clear_oled()
                add_text(0, 0, "Error")

                # Dont set a response message in order
                # To listen for a new
                messageReturn = None

            # Send response
            if messageReturn != None:
                send_msg(messageReturn)

    # When press A, initialize a communication or stop it
    # Depends of the value of com_established
    if button_a.was_pressed():
        if com_established == False:
            send_msg(init)
        else:
            com_established = manage_protocol(stop, com_established)
##################################################
