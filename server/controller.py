# Program to control passerelle between Android application
# and micro-controller through USB tty
import time
import argparse
import signal
import sys
import socket
import socketserver
import serial
import threading
import time
from pymongo import MongoClient
import json

client = MongoClient("mongodb://admin:secure@localhost:27017/admin")
db = client.admin
collection = db['iot']

HOST           = "192.168.1.53"
UDP_PORT       = 10000
MICRO_COMMANDS = ["TL" , "LT"]
FILENAME        = "values.txt"
LAST_VALUE      = b"TL"
LAST_CLIENT_ADDRESS = ""
LAST_SOCKET = ""
LAST_VALUE_RECEIVED = ""

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global LAST_CLIENT_ADDRESS
        global LAST_SOCKET
        global LAST_VALUE_RECEIVED
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        if data != "":
                        if str(data, 'UTF-8') in MICRO_COMMANDS: # Send message through UART
                                str_data = str(data, 'UTF-8') + "\n"
                                print(str_data)
                                LAST_VALUE_RECEIVED = str_data
                                LAST_CLIENT_ADDRESS = (self.client_address[0], 10000)
                                LAST_SOCKET = socket
                                sendUARTMessage(str.encode(str_data))

                        elif str(data,'UTF-8') == "getValues()": # Sent last value received from micro-controller
                                socket.sendto(LAST_VALUE, self.client_address)
                                # TODO: Create last_values_received as global variable
                        else:
                                print("Unknown message: ",data)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


# send serial message
SERIALPORT = "/dev/ttyACM0"
BAUDRATE = 115200
ser = serial.Serial()

def initUART():
        # ser = serial.Serial(SERIALPORT, BAUDRATE)
        ser.port=SERIALPORT
        ser.baudrate=BAUDRATE
        ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        ser.parity = serial.PARITY_NONE #set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        ser.timeout = None          #block read

        # ser.timeout = 0             #non-block read
        # ser.timeout = 2              #timeout block read
        ser.xonxoff = False     #disable software flow control
        ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        #ser.writeTimeout = 0     #timeout for write
        print('Starting Up Serial Monitor')
        try:
                ser.open()
        except serial.SerialException:
                print("Serial {} port not available".format(SERIALPORT))
                exit()



def sendUARTMessage(msg):
    ser.write(msg)
    display = str(msg, 'UTF-8')
    print("Message <" + display + "> sent to micro-controller." )


# Main program logic follows:
if __name__ == '__main__':
        initUART()
        f= open(FILENAME,"a")
        print ('Press Ctrl-C to quit.')

        server = ThreadedUDPServer((HOST, UDP_PORT), ThreadedUDPRequestHandler)

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True

        try:
                server_thread.start()
                print("Server started at {} port {}".format(HOST, UDP_PORT))
                while ser.isOpen() :
                        # time.sleep(100)
                        if (ser.inWaiting() > 0): # if incoming bytes are waiting
                                #data_b = ser.read(ser.inWaiting())
                                data_b = ser.readline()
                                data_str = str(data_b, 'UTF-8')
                                if data_str == "retry\n":
                                    sendUARTMessage(str.encode(LAST_VALUE_RECEIVED))
                                    print("retry <" + LAST_VALUE_RECEIVED + ">")
                                else:
                                    LAST_VALUE = data_b
                                    f.write(data_str)
                                    collection.insert_one(json.loads(data_str))
                                    if(LAST_SOCKET != ""):
                                        LAST_SOCKET.sendto(data_b, LAST_CLIENT_ADDRESS)
                                    print(data_str)
        except (KeyboardInterrupt, SystemExit):
                server.shutdown()
                server.server_close()
                f.close()
                ser.close()
                exit()
