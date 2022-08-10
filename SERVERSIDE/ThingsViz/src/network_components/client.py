import csv
import time
import random
import argparse
import mqtt_functions as mqtt


class dataSender:
    def __init__(self, addressOfBroker, portOfBroker, topicGroup, sleeptime):
        self.addressOfBroker = addressOfBroker
        self.portOfBroker = portOfBroker
        self.server_address = (self.addressOfBroker, self.portOfBroker)
        self.clientID = f'python-mqtt-{random.randint(0, 1000)}'     

        self.topicGroup = topicGroup
        self.username = "vv8cQBxJLeaZ0JpIUpFP"
        self.password = "nopassword"

        self.sleeptime = sleeptime
        self.legal_SF_ALLOC = [1,2,3,4,5,6]
        self.legal_SF_PERIOD = [1,2,4,8,16,32]
        
    def run(self):
        while True:
            newParametersToSend = self.generateNewRandomFrame()
            self.sendNewParametersToBroker(newParametersToSend)
            time.sleep(self.sleeptime)

    def sendNewParametersToBroker(self, newParametersToSend):
        client = mqtt.connectToBroker(self.clientID, self.username, self.password, self.addressOfBroker, self.portOfBroker)
        mqtt.publishParameters(client, newParametersToSend)

    def generateNewRandomFrame(self):
            SF_ALLOC = random.choice(self.legal_SF_ALLOC)
            SF_PERIOD = random.choice(self.legal_SF_PERIOD)
            PERCENTAGE = random.randint(0, 100)
            return {"SF_ALLOC": SF_ALLOC, "SF_PERIOD": SF_PERIOD, "PERCENTAGE": PERCENTAGE}

def main(addressOfBroker, portOfBroker, topicGroup, sleeptime):
    generator = dataSender(addressOfBroker, portOfBroker, topicGroup, sleeptime)
    generator.run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a random data generator client')
    parser.add_argument('--addressOfBroker', type=str, required=False, default= "henri-zbook",
                        help='address of the broker')              
    parser.add_argument('--portOfBroker', type=int, required=False, default= 1883,
                        help='port of the broker')
    parser.add_argument('--topicGroup', type=str, required=False, default= "ThingsViz/parameters",
                        help='topic to publish on')
    parser.add_argument('--sleeptime', type=float, required=False, default= 0.64,
                        help='time between sending new rowes')
    args = parser.parse_args()
    main(addressOfBroker = args.addressOfBroker,portOfBroker = args.portOfBroker, topicGroup = args.topicGroup, sleeptime = args.sleeptime)

