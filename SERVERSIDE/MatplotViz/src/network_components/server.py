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