import argparse
import functions_socket as socket
import functions_mqtt as mqtt
#INFO: Listens for messages recieved from client and publishes them to the mqtt broker.

class Server:
    def __init__(self, addressOfBroker, portOfBroker, topicGroup, addressOfServer, portOfServer, sleeptime):
        # MQTT BROKER VALUES
        self.addressOfBroker = addressOfBroker
        self.portOfBroker = portOfBroker
        self.clientID = "THISISHENRIZBOOKDEVICEID"     
        self.topicGroup = topicGroup
        self.username = "CGO0qUUI1BiPOkUhkYy7"
        self.password = "nopassword"

        # SOCKET VALUES
        self.addressOfServer = addressOfServer
        self.portOfServer = portOfServer
        self.socket = socket.initiateSocket(self.addressOfServer, self.portOfServer)
        
    def run(self):
        while True:
            newParametersToSend = socket.listenForNewMessage(self.socket)
            mqtt.sendNewParametersToBroker(newParametersToSend, self.clientID, self.username, self.password, self.addressOfBroker, self.portOfBroker, self.topicGroup)
    
def main(addressOfBroker, portOfBroker, topicGroup, addressOfServer, portOfServer, sleeptime):
    generator = Server(addressOfBroker, portOfBroker, topicGroup, addressOfServer, portOfServer, sleeptime)
    generator.run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a random data generator client')
    parser.add_argument('--addressOfBroker', type=str, required=False, default= "thingsboard.cloud",
                        help='address of the broker')              
    parser.add_argument('--portOfBroker', type=int, required=False, default= 1883,
                        help='port of the broker')
    parser.add_argument('--topicGroup', type=str, required=False, default= "ThingsViz/telemetry",
                        help='topic to publish on')
    parser.add_argument('--addressOfServer', type=str, required=False, default= "localhost",
                        help='Address of serversocket')
    parser.add_argument('--portOfServer', type=int, required=False, default= 10000,
                        help='Port of serversocket')
    parser.add_argument('--sleeptime', type=float, required=False, default= 0.64,
                        help='time between sending new rowes')
    args = parser.parse_args()
    main(addressOfBroker = args.addressOfBroker,portOfBroker = args.portOfBroker, topicGroup = args.topicGroup, addressOfServer = args.addressOfServer, portOfServer = args.portOfServer, sleeptime = args.sleeptime)

