# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client

def connectToBroker(clientID, username, password, addressOfBroker, portOfBroker):
    client = setConnectionParameters(clientID, username, password, addressOfBroker, portOfBroker)
    return client

def setConnectionParameters(clientID, username, password, addressOfBroker, portOfBroker):
    client = mqtt_client.Client(clientID)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(addressOfBroker, portOfBroker)
    return client

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code " + str(rc))

def publishParameters(client, newParametersToSend, topicGroup):
    client.loop()
    newMQTTmsg = wrapParametersIntoMQTTmsg(newParametersToSend)
    client.publish(topicGroup, newMQTTmsg) 
    print("Sending " + newMQTTmsg + " to topic " + topicGroup)  
    print("--------------------------------------------------------------------------------------------------")

def wrapParametersIntoMQTTmsg(newParametersToSend):
    SF_ALLOC, SF_PERIOD, PERCENTAGE = newParametersToSend
    DICTmsg = {"SF_ALLOC": SF_ALLOC, "SF_PERIOD": SF_PERIOD, "PERCENTAGE": PERCENTAGE}
    return constructMQTTmsg(DICTmsg)

def constructMQTTmsg(DICTmsg):
    totalMessage = "{"
    for parameterName in DICTmsg.keys():
        parameterKeyValuePair = '"' +  parameterName + '":' + str(DICTmsg[parameterName])
        totalMessage += parameterKeyValuePair + ","
    totalMessage = totalMessage[:-1] +  "}" 
    return totalMessage