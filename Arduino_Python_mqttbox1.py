import pyfirmata
import os
import serial
from datetime import datetime
import imaplib
import sys
import paho.mqtt.client as mqtt
import threading
import poplib
import email
import time
from logininfo import user
from logininfo import password
from logininfo import mindsphere_id
from logininfo import client_address


# Def Variables
A0 = 2
Status = 0
board = pyfirmata.Arduino('/dev/ttyACM0')                                                                      #Define your board with serial port

it = pyfirmata.util.Iterator(board)                                                                    # assigns an iterator which is used to read the status of the inputs of the circuit.
it.start()                                                                                             # atarts the iterator

board.digital[7].mode = pyfirmata.INPUT                                                                # sets pin 7 as digital input with + pyfirmata.INPUT +. This is necessary because in the standard configuration digital pins are used as outputs.
analog_output0 = board.get_pin('a:0:o')                                                                # get the information from analog pin number 0. the o stands for output. T0
analog_output1 = board.get_pin('a:1:o')                                                                # get the information from analog pin number 1. the o stands for output T1

time.sleep(1) #needs this pause... for some reason

while True:
    A0 = analog_output0.read()                                                                          # read the information of pin0 (it is a voltage of temperature sensor TO)
    print("V0" + str(A0))
    dummy_data = "200,CurentTemperature,T0," + str(A0 * 1000).strip() + ",degree"                            #PAYLOAD of Temperature T0 for MindSphere
    print(dummy_data)

    # create MQTT Client and connect to MindShpere MQTT Broker
    client = mqtt.Client(client_id = mindsphere_id)                          #create client. Cient ID from MQTTBox!
    client.username_pw_set(user, password)                   #MindSphere user name and pw - David will sent it to you
    client.connect(client_address, 1883)                            #connect to client of MindSphere. use your tenant
    client.loop_start()
    client.publish("s/us", "100,CO2+Arduino,MCIoT_MQTTDevice")                        #send information to MindSphere IOT extension with device information
    client.publish("s/us", "110," + mindsphere_id +",Arduino and Lenovo,0.1")       #send information to MindSphere IOT extension with your client ID, System and Rev Number)
    client.publish("s/us", "112,59.3293,18.0686,50,1")
    client.subscribe("s/ds")
    client.publish("s/us",dummy_data)                                                                   #send Temp T0 data to MindSphere
    '''
    file = open ("Temperatureausgabe.txt","w")
    file.write(messdaten)
    file.write("°C")
    file.write("\n")
    '''

    time.sleep(1)



