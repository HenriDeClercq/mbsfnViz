import argparse
import functions_csv as csv
import functions_socket as socket
#INFO: Listens for messages recieved from client and pushes them to a csv file.

class Server:
    def __init__(self, addressOfServer, portOfServer, filename):
        # CSV FILE VALUES
        self.filename = "csv_files/" + filename
        self.filelock = csv.initiateFileLock(self.filename)
        self.INDEX = csv.initiateCSVFile(self.filename, self.filelock)

        # SOCKET VALUES
        self.addressOfServer = addressOfServer
        self.portOfServer = portOfServer
        self.socket = socket.initiateSocket(self.addressOfServer, self.portOfServer)
        
    def run(self):
        while True:
            SF_ALLOC, SF_PERIOD, PERCENTAGE = socket.listenForNewMessage(self.socket)
            newRowToAppend = [self.INDEX, SF_ALLOC, SF_PERIOD, PERCENTAGE]
            self.INDEX = csv.appendNewRowToFile(self.filename, self.filelock, newRowToAppend, "append")
   
def main(addressOfServer, portOfServer, filename):
    generator = Server(addressOfServer, portOfServer, filename)
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

