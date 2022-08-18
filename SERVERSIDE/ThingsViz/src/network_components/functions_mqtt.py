from paho.mqtt import client as mqtt_client
import json
#from datetime import datetime 
#import time

def sendNewParametersToBroker(newParametersToSend, clientID, username, password, addressOfBroker, portOfBroker, topicGroup):
        client = connectToBroker(clientID, username, password, addressOfBroker, portOfBroker)
        publishParameters(client, newParametersToSend, topicGroup)   

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
    newMQTTmsg = wrapParametersIntoMQTTmsg(newParametersToSend)
    client.loop()
    client.publish(topicGroup, newMQTTmsg) 
    print("Sending " + newMQTTmsg + " to topic " + topicGroup)  
    print("--------------------------------------------------------------------------------------------------")

def wrapParametersIntoMQTTmsg(newParametersToSend):
    SF_ALLOC, SF_PERIOD, PERCENTAGE = newParametersToSend
    DICTparameters = {"SF_ALLOC": SF_ALLOC, "SF_PERIOD": SF_PERIOD, "PERCENTAGE": PERCENTAGE}
    return convertDictionaryToMQTTmsg(DICTparameters)
    #TODO: SEND CUSTOM TIMESTAMP IN HEADER #######################################################################
    #DICTmsg = {"ts": time.mktime(datetime.now().timetuple()), "values": DICTparameters}
    #return convertDictionaryToMQTTmsg(DICTmsg)

def convertDictionaryToMQTTmsg(DICTmsg):
    return json.dumps(DICTmsg)