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
from random import randint


# Def Variables
A0 = 2
Status = 0
board = pyfirmata.Arduino('/dev/ttyACM0')                                                                      #Define your board with serial port

it = pyfirmata.util.Iterator(board)                                                                    # assigns an iterator which is used to read the status of the inputs of the circuit.
it.start()                                                                                             # atarts the iterator

board.digital[7].mode = pyfirmata.INPUT                                                                # sets pin 7 as digital input with + pyfirmata.INPUT +. This is necessary because in the standard configuration digital pins are used as outputs.
analog_output0 = board.get_pin('a:0:o')                                                                # get the information from analog pin number 0. the o stands for output. T0
analog_output1 = board.get_pin('a:1:o')                                                                # get the information from analog pin number 1. the o stands for output T1

CO_value = 0
LPG_value = 0
CH4_value = 0
C3H8_value = 0

time.sleep(1) #needs this pause... for some reason

while True:
    #Read data/emissions from Sensors and store in payload format ready to be published later
    CO2_raw_value = analog_output0.read()
    CO2_value = CO2_raw_value * 1000
    CO2_payload = "200,CO2 Emissions,CO2," + str(CO2_value).strip() + ",tonnes"
    print(CO2_payload)

    rand_num = randint(-10, 10)
    CO_value += rand_num
    if CO_value < 0:
        CO_value = 0 
    if CO_value > 500:
        CO_value = 500 
    CO_payload = "200,CO Emissions,CO," + str(CO_value).strip() + ",tonnes"
    print(CO_payload)

    rand_num = randint(-10, 10)
    LPG_value += rand_num
    if LPG_value < 0:
        LPG_value = 0 
    if LPG_value > 500:
        LPG_value = 500 
    LPG_payload = "200,LPG Emissions,LPG," + str(LPG_value).strip() + ",tonnes"
    print(LPG_payload)

    rand_num = randint(-10, 10)
    CH4_value += rand_num
    if CH4_value< 0:
        CH4_value = 0 
    if CH4_value > 500:
        CH4_value = 500 
    CH4_payload = "200,CH4 Emissions,CH4," + str(CH4_value).strip() + ",tonnes"
    print(CH4_payload)

    rand_num = randint(-10, 10)
    C3H8_value += rand_num
    if C3H8_value< 0:
        C3H8_value = 0 
    if C3H8_value > 500:
        C3H8_value = 500 
    C3H8_payload = "200,C3H8 Emissions,LPG," + str(C3H8_value).strip() + ",tonnes"
    print(C3H8_payload)
    print("\n")

    # create MQTT Client and connect to MindShpere MQTT Broker
    client = mqtt.Client(client_id = mindsphere_id)                          #create client. Cient ID from MQTTBox!
    client.username_pw_set(user, password)                   #MindSphere user name and pw - David will sent it to you
    client.connect(client_address, 1883)                            #connect to client of MindSphere. use your tenant
    client.loop_start()

    client.publish("s/us", "100,CO2 Stockholm,MCIoT_MQTTDevice")                        #send information to MindSphere IOT extension with device information
    client.publish("s/us", "110," + mindsphere_id +",Arduino and Lenovo,0.1")       #send information to MindSphere IOT extension with your client ID, System and Rev Number)
    client.publish("s/us", "112,59.3293,18.0686,50,1")
    client.subscribe("s/ds")

    #Individual publishing first. The last one published will be the first one shown in Mindsphere
    client.publish("s/us", C3H8_payload)
    client.publish("s/us", CH4_payload)
    client.publish("s/us", LPG_payload)
    client.publish("s/us", CO_payload)
    client.publish("s/us", CO2_payload)
    
    #Group Publishing. All in one same chart called "All Emissions"
    C3H8_payload_group = "200,All Emissions,C3H8," + str(C3H8_value).strip() + ",tonnes"
    CH4_payload_group = "200,All Emissions,CH4," + str(CH4_value).strip() + ",tonnes"
    LPG_payload_group = "200,All Emissions,LPG," + str(LPG_value).strip() + ",tonnes"
    CO2_payload_group = "200,All Emissions,CO2," + str(CO2_value).strip() + ",tonnes"
    CO_payload_group = "200,All Emissions,CO," + str(CO_value).strip() + ",tonnes"
    client.publish("s/us", C3H8_payload_group)
    client.publish("s/us", CH4_payload_group)
    client.publish("s/us", LPG_payload_group)
    client.publish("s/us", CO_payload_group)
    client.publish("s/us", CO2_payload_group)
    '''
    file = open ("Temperatureausgabe.txt","w")
    file.write(messdaten)
    file.write("°C")
    file.write("\n")
    '''

    time.sleep(1)



