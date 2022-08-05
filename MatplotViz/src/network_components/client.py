import csv
import time
import random
import argparse
import socket
from filelock import FileLock, Timeout

class dataSender:
    def __init__(self, addressOfServer, portOfServer, sleeptime, filename = "csv_files/random_generated.csv"):
        self.filename = filename
        self.filelockname = filename+".lock"
        self.filelock = FileLock(self.filelockname, timeout=1)
        self.addressOfServer = addressOfServer
        self.portOfServer = portOfServer
        self.server_address = (self.addressOfServer, self.portOfServer)
        
        self.sleeptime = sleeptime
        self.legal_SF_ALLOC = [1,2,3,4,5,6]
        self.legal_SF_PERIOD = [1,2,4,8,16,32]
        
    def run(self):
        while True:
            SF_ALLOC, SF_PERIOD, PERCENTAGE = self.generateNewRandomFrame()
            newRowToAppend = [SF_ALLOC, SF_PERIOD, PERCENTAGE]
            self.sendNewRowToServer(newRowToAppend)
            time.sleep(self.sleeptime)

    def sendNewRowToServer(self, newRowToAppend):
        newSocket = self.initiateSocket()
        #print("Connection to server on %s port %s" % self.server_address)
        newSocket.connect(self.server_address)
        try:
            print("Sending: " + str(newRowToAppend))
            bytesToSend = str.encode(str(newRowToAppend[0]) + "," + str(newRowToAppend[1]) + "," + str(newRowToAppend[2]))
            newSocket.sendall(bytesToSend)
        finally:
            #print("Closing connection...")
            newSocket.close()

    def generateNewRandomFrame(self):
            SF_ALLOC = random.choice(self.legal_SF_ALLOC)
            SF_PERIOD = random.choice(self.legal_SF_PERIOD)
            PERCENTAGE = 60.2
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

