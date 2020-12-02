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

client = MongoClient("mongodb://admin:secure@localhost:27017/admin") # Connexion au client mongodb, l'url diffère en fonction de l'environnement
db = client.admin # récupération de la base admin
collection = db['iot'] # récupération de la collection 'iot' c'est dans cette collection qu'on stocke nos données

HOST           = "192.168.1.53" #adresse ip sur laquelle le serveur est lancée, elle correspond obligatoirement à l'adresse locale de l'ordinateur sur le réseau
UDP_PORT       = 10000 # port udp par défaut pour les communications avec l'appli android
MICRO_COMMANDS = ["TL" , "LT"] #list des commandes acceptées par le serveur en provenance de l'appli android
FILENAME        = "values.txt"  # fichier texte utilisé pour stocker les données (useless now car on a mongo)
LAST_VALUE      = b"TL" #derniere valeur remontée par le microbit (initialisée a TL arbitrairement) elle prend des valeurs json type : {t: 28, l: 0, o: "TL"}
LAST_CLIENT_ADDRESS = "" #adresse du dernier client android avec qui le serveur a communiqué
LAST_SOCKET = "" # socket utilisé avec le dernier client android
LAST_VALUE_RECEIVED = "" # dernière valeur recue par un client android ("LT" ou "TL")

#Cette classe est executée as a thread et permet de traiter les échanges entre le serveur et le client android qui s'y connecte
class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

     #cette methode est executée dès lors que le serveur reçoit un message UDP 
    def handle(self):
        global LAST_CLIENT_ADDRESS #mot clé global pour faire référence à la variable globale settée plus haut
        global LAST_SOCKET
        global LAST_VALUE_RECEIVED
        data = self.request[0].strip() # récuperation des données envoyé par l'app ("LT" ou "TL")
        socket = self.request[1] # recuperation du socket envoyé 
        current_thread = threading.current_thread() #création du thread pour handle la requête
        print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data)) #affichage console pour dire qu'on a reçu un message udp d'une app
        if data != "":
                        if str(data, 'UTF-8') in MICRO_COMMANDS: # Send message through UART
                                str_data = str(data, 'UTF-8') + "\n" # conversion de la donnée + ajout d'un \n pour le readline (fonction qui lit jusquau premier \n)
                                print(str_data)
                                #sauvegard des valeurs, adresse et socket de cette requête
                                LAST_VALUE_RECEIVED = str_data 
                                LAST_CLIENT_ADDRESS = (self.client_address[0], 10000)
                                LAST_SOCKET = socket

                                #envoi d'un message au microbit via l'uart comprenant "TL" ou "LT"
                                sendUARTMessage(str.encode(str_data))
                        # valeur inconnue recue
                        else:
                                print("Unknown message: ",data)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


# send serial message
SERIALPORT = "/dev/ttyACM0" # port serie du microbit connecté via usb (ttyACMX pour linux, COMXX pour windows)
BAUDRATE = 115200 # baudrate par defaut
ser = serial.Serial() # recuperation de la connexion serie

#methode d'initialisation de la connexion UART
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


# methode d'envoi d'un message par UART (a destination du microbit)
def sendUARTMessage(msg):
    ser.write(msg) # envoi du message
    display = str(msg, 'UTF-8')
    print("Message <" + display + "> sent to micro-controller." ) #retour visuel dans la console du serveur


# Main program logic follows:
if __name__ == '__main__':
        initUART() # initialisation uart
        f= open(FILENAME,"a") # ouverture du fichier texte, un peu useless maintenant car mongo
        print ('Press Ctrl-C to quit.')

        server = ThreadedUDPServer((HOST, UDP_PORT), ThreadedUDPRequestHandler) # création du serveur

        #initialisation du thread du serveur
        server_thread = threading.Thread(target=server.serve_forever) 
        server_thread.daemon = True

        try:
                server_thread.start() #lancement du serveur en attente de requêtes (uart + udp) + retour visuel
                print("Server started at {} port {}".format(HOST, UDP_PORT))
                while ser.isOpen() :
                        if (ser.inWaiting() > 0): # if incoming bytes are waiting
                                data_b = ser.readline() # recuperation des données en provenance de l'UART (microbit)
                                data_str = str(data_b, 'UTF-8') #conversion des bits en string
                                if data_str == "retry\n": #si une erreur est survenue = le microbit renvoie "retry\n"
                                    sendUARTMessage(str.encode(LAST_VALUE_RECEIVED)) # alors on renvoie le dernier message envoyé pour relancer l'operation
                                    print("retry <" + LAST_VALUE_RECEIVED + ">") # retour visuel
                                else:
                                    LAST_VALUE = data_b # sinon, tout s'est bien passé et on a reçu des données depuis le microbit
                                    f.write(data_str) # on écrit ces données dans le fichier texte
                                    collection.insert_one(json.loads(data_str)) # on les sauvegarde en bdd
                                    if(LAST_SOCKET != ""):
                                        LAST_SOCKET.sendto(data_b, LAST_CLIENT_ADDRESS) # puis on envoi ces données à l'application
                                    print(data_str)
        except (KeyboardInterrupt, SystemExit): # en cas de ctrl+c on close tout et on quitte
                server.shutdown()
                server.server_close()
                f.close()
                ser.close()
                exit()
