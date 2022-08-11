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
        #print("Connection to server on %s port %s" % self.server_address)
        newSocket.connect(self.server_address)
        try:
            print("Sending: " + str(newParameters))
            bytesToSend = str.encode(str(newParameters[0]) + "," + str(newParameters[1]) + "," + str(newParameters[2]))
            newSocket.sendall(bytesToSend)
        finally:
            #print("Closing connection...")
            newSocket.close()

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
    parser.add_argument('--sleeptime', type=float, required=False, default= 0.5,
                        help='time between sending new rowes')
    args = parser.parse_args()
    main(addressOfServer = args.addressOfServer, portOfServer = args.portOfServer, sleeptime = args.sleeptime)

