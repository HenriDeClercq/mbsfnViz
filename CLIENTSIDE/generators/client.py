import csv
import time
import random
import argparse
import socket
#INFO: Generates random parameters and sends them to the socket.

class dataSender:
    def __init__(self, addressOfServer, portOfServer, sleeptime):
        self.addressOfServer = addressOfServer
        self.portOfServer = portOfServer
        self.server_address = (self.addressOfServer, self.portOfServer)
        
        self.sleeptime = sleeptime
        self.legal_SF_ALLOC = [1,2,3,4,5,6]
        self.legal_SF_PERIOD = [1,2,4,8,16,32]
        
    def run(self):
        while True:
            newParameters = self.generateNewRandomFrame()
            self.sendNewParametersToServer(newParameters)
            time.sleep(self.sleeptime)

    def sendNewParametersToServer(self, newParameters):
        newSocket = self.initiateSocket()
        newSocket.connect(self.server_address)
        try:
            self.encodeAndSendParameters(newSocket, newParameters)
        finally:
            newSocket.close()

    def encodeAndSendParameters(self, socket, parameters):
            print("Sending: " + str(parameters))
            bytesToSend = str.encode(str(parameters[0]) + "," + str(parameters[1]) + "," + str(parameters[2]))
            socket.sendall(bytesToSend)

    def generateNewRandomFrame(self):
            SF_ALLOC = random.choice(self.legal_SF_ALLOC)
            SF_PERIOD = random.choice(self.legal_SF_PERIOD)
            PERCENTAGE = random.randint(0,100)
            return (SF_ALLOC, SF_PERIOD, PERCENTAGE)

    def initiateSocket(self):
        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return newSocket

def main(addressOfServer, portOfServer, sleeptime):
    generator = dataSender(addressOfServer, portOfServer, sleeptime)
    generator.run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a random data generator client')
    parser.add_argument('--addressOfServer', type=str, required=False, default= "localhost",
                        help='time between sending new rowes')
    parser.add_argument('--portOfServer', type=int, required=False, default= 10000,
                        help='time between sending new rowes')
    parser.add_argument('--sleeptime', type=float, required=False, default= 0.64,
                        help='time between sending new rowes')
    args = parser.parse_args()
    main(addressOfServer = args.addressOfServer, portOfServer = args.portOfServer, sleeptime = args.sleeptime)

