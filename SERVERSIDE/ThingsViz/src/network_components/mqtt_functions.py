# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


addressOfBroker = 'henri-zbook'
portOfBroker = 1883
topic = "v1/devices/me/telemetry"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = "vv8cQBxJLeaZ0JpIUpFP"
password = "nopassword"

#def connectToBroker(client_id, username, password, addressOfBroker, portOfBroker):
def connectToBroker(clientID, username, password, saddressOfBroker, portOfBroker):
    client = setConnectionParameters()
    return client

def setConnectionParameters():
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(addressOfBroker, portOfBroker)
    return client

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def publishParameters(client, newParametersToSend):
    client.loop()
    client.publish("v1/devices/me/telemetry", newParametersToSend) 
    print("Sending " + newParametersToSend + " to topic " + topic)  
    print("--------------------------------------------------------------------------------------------------")

def wrapParametersIntoMQTTmsg(SF_ALLOC, SF_PERIOD, PERCENTAGE):
    DICTmsg = {"SF_ALLOC": SF_ALLOC, "SF_PERIOD": SF_PERIOD, "PERCENTAGE": PERCENTAGE}
    MQTTmsg = constructMQTTmsg(DICTmsg)

def constructMQTTmsg(DICTmsg):
    totalMessage = "{"
    for parameterName in DICTmsg.keys():
        parameterKeyValuePair = '"' +  parameterName + '":' + str(DICTmsg[parameterName])
        totalMessage += parameterKeyValuePair + ","
    totalMessage = totalMessage[:-1] +  "}" 
    return totalMessage