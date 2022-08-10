import csv
import time
import argparse
import random
import mqtt_functions as mqtt
# RECIEVES FROM SOCKET AND SENDS TO MQTT BROKER

class dataReciever:
    def __init__(self, addressOfBroker, portOfBroker, topicGroup):
        self.addressOfBroker = addressOfBroker
        self.portOfBroker = portOfBroker
        self.server_address = (self.addressOfBroker, self.portOfBroker)
        self.clientID = f'python-mqtt-{random.randint(0, 1000)}'     

        self.topicGroup = topicGroup
        self.username = "vv8cQBxJLeaZ0JpIUpFP"
        self.password = "nopassword"

        
    def run(self):
        while True:
            SF_ALLOC, SF_PERIOD, PERCENTAGE = self.listenForNewMessage()
            MQTTmsgToSend = mqtt.wrapParametersIntoMQTTmsg(SF_ALLOC, SF_PERIOD, PERCENTAGE)
            self.sendNewParametersToBroker(MQTTmsgToSend)

    def sendNewParametersToBroker(self, newParametersToSend):
        client = mqtt.connectToBroker(self.clientID, self.username, self.password, self.addressOfBroker, self.portOfBroker)
        mqtt.publishParameters(client, newParametersToSend)

    def copyOldFileValues(self, writemode):
        data = []
        if writemode == "append":
            with open(self.filename, 'r') as read_obj:
                csv_reader = csv.reader(read_obj)
                for row in csv_reader:
                    data.append(row) 
        return data
    
    def overwriteOldFileValues(self, newDataValues):
            with open(self.filename, 'w', newline='') as file:
                mywriter = csv.writer(file, delimiter=',')
                mywriter.writerows(newDataValues)
            print(str(self.INDEX) + ": New row appended to file...")

    def listenForNewMessage(self):
        connection, client_address = self.listenForAndAcceptNewConnection()
        try:
            SF_ALLOC, SF_PERIOD, PERCENTAGE = self.recieveMessageFromConnectedClient(connection)
        finally:
            connection.close()
            return SF_ALLOC, SF_PERIOD, PERCENTAGE

    def listenForAndAcceptNewConnection(self):
        self.socket.listen(1)
        connection, client_address = self.socket.accept() 
        return connection, client_address

    def recieveMessageFromConnectedClient(self, connection):
        dataInBytes = connection.recv(16)
        dataInString = dataInBytes.decode()
        SF_ALLOC, SF_PERIOD, PERCENTAGE = dataInString.split(",")
        print("-----------------------------------------------------------------------------")
        print("Received: " + dataInString)
        return int(SF_ALLOC), int(SF_PERIOD), float(PERCENTAGE)
        
def main(addressOfServer, portOfServer, filename):
    generator = dataReciever(addressOfServer, portOfServer, filename)
    generator.run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a random data generator client')
    parser.add_argument('--addressOfServer', type=str, required=False, default= "localhost",
                        help='Address of serversocket')
    parser.add_argument('--portOfServer', type=int, required=False, default= 10000,
                        help='Port of serversocket')
    parser.add_argument('--filename', type=str, required=False, default= "default.csv",
                        help='the path to the csv filename')
    args = parser.parse_args()
    main(addressOfServer = args.addressOfServer, portOfServer = args.portOfServer, filename = args.filename)
