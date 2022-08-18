import functions_socket as socket
import functions_mqtt as mqtt
#INFO: Listens for messages recieved from client and publishes them to the mqtt broker.

class Server:
    def __init__(self, addressOfBroker, portOfBroker, deviceAccessToken, topicGroup, addressOfServer, portOfServer):
        # MQTT BROKER VALUES
        self.addressOfBroker = addressOfBroker
        self.portOfBroker = portOfBroker  
        self.topicGroup = topicGroup
        self.username = deviceAccessToken
        self.password = "nopassword"
        self.clientID = "THISISTHEUNIQUESERVERID"   

        # SOCKET VALUES
        self.addressOfServer = addressOfServer
        self.portOfServer = portOfServer
        self.socket = socket.initiateSocket(self.addressOfServer, self.portOfServer)
        
    def run(self):
        while True:
            newParametersToSend = socket.listenForNewMessage(self.socket)
            mqtt.sendNewParametersToBroker(newParametersToSend, self.clientID, self.username, self.password, self.addressOfBroker, self.portOfBroker, self.topicGroup)