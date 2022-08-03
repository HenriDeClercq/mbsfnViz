import csv
import time
import argparse
from filelock import FileLock, Timeout
import socket
# RECIEVES FROM SOCKET AND WRITES TO CSV FILE

class dataReciever:
    def __init__(self, address, port, filename = "csv_files/random_generated.csv"):
        self.address = address
        self.port = port
        self.filename = filename
        self.filelockname = filename+".lock"
        self.filelock = FileLock(self.filelockname, timeout=1)
        self.INDEX = 0
        self.socket = self.initiateSocket()

        self.legal_WRITEMODES = ["initialize", "append"]
        self.appendNewRowToFile(["FRAME_ID","SF_ALLOC", "SF_PERIOD"], "initialize")
        
    def run(self):
        while True:
            SF_ALLOC, SF_PERIOD = self.listenForNewMessage()
            newRowToAppend = [self.INDEX, SF_ALLOC, SF_PERIOD]
            self.appendNewRowToFile(newRowToAppend, "append")

    def appendNewRowToFile(self, newRowToAppend, writemode):
        self.filelock.acquire()
        try:
            self.checkIfLegalWriteMode(writemode)
            data = self.copyOldDataValues(writemode)     
            data.append(newRowToAppend)
            self.overwriteOldFileValues(data)
        finally:
            self.filelock.release()

    def checkIfLegalWriteMode(self, writemode):
        if not (writemode in self.legal_WRITEMODES):
            print("ILLEGAL WRITEMODE")
            return

    def copyOldDataValues(self, writemode):
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
            SF_ALLOC, SF_PERIOD = self.recieveMessageFromConnectedClient(connection)
        finally:
            connection.close()
            self.INDEX += 1
            return SF_ALLOC, SF_PERIOD

    def listenForAndAcceptNewConnection(self):
        self.socket.listen(1)
        connection, client_address = self.socket.accept() 
        return connection, client_address

    def recieveMessageFromConnectedClient(self, connection):
        dataInBytes = connection.recv(16)
        dataInString = dataInBytes.decode()
        SF_ALLOC, SF_PERIOD = dataInString.split(",")
        print("-----------------------------------------------------------------------------")
        print("Received: " + dataInString)
        return int(SF_ALLOC), int(SF_PERIOD)
        
    def initiateSocket(self):
        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.address, self.port)
        print("starting up on %s port %s" % server_address)
        newSocket.bind(server_address)
        return newSocket
    
def main(addressOfServer, portOfServer):
    generator = dataReciever(addressOfServer, portOfServer)
    generator.run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a random data generator client')
    parser.add_argument('--addressOfServer', type=str, required=False, default= "localhost",
                        help='Address of serversocket')
    parser.add_argument('--portOfServer', type=int, required=False, default= 10000,
                        help='Port of serversocket')
    args = parser.parse_args()
    main(addressOfServer = args.addressOfServer, portOfServer = args.portOfServer)

