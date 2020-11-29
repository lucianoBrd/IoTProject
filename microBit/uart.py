# Import libraries
##################################################
from microbit import *
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
# Values we can receive by the uart
acceptedCommands = ['LT', 'TL']
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

# Config the uart
##################################################
uart.init(baudrate=115200, bits=5096)
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
    else:
        i=0
        isSent = False
        messageUart = uart.readline()
        
        if (messageUart != None):
            messageUartStr = str(messageUart, 'UTF-8')
            messageUartStr = messageUartStr[0:2]
            if messageUartStr in acceptedCommands:
                while (isSent == False):
                    send_msg(messageUartStr)
                    
                    message = None
                    i=0
                    while(message == None):
                        message = listen()
                        if (message != None):
                            uart.write(message+"\n")
                            isSent = True
                            messageUart = None
                            break
                        i += 1
                        if (i > 5000): 
                            break
            else:
                uart.write("retry\n")
                messageUart = None

    # When press A, initialize a communication or stop it
    # Depends of the value of com_established
    if button_a.was_pressed():
        if com_established == False:
            send_msg(init)
        else:
            com_established = manage_protocol(stop, com_established)
##################################################
