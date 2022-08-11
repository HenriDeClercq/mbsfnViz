import socket

def listenForNewMessage(Socket):
    newConnection = listenForAndAcceptNewConnection(Socket)
    try:
        SF_ALLOC, SF_PERIOD, PERCENTAGE = recieveMessageFromConnectedClient(newConnection)
    finally:
        newConnection.close()
        return SF_ALLOC, SF_PERIOD, PERCENTAGE

def listenForAndAcceptNewConnection(Socket):
    Socket.listen(1)
    connection, client_address = Socket.accept() 
    return connection

def recieveMessageFromConnectedClient(connection):
    dataInBytes = connection.recv(16)
    dataInString = dataInBytes.decode()
    SF_ALLOC, SF_PERIOD, PERCENTAGE = dataInString.split(",")
    print("Received: " + dataInString)
    return int(SF_ALLOC), int(SF_PERIOD), int(PERCENTAGE)
        
def initiateSocket(addressOfServer, portOfServer):
    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (addressOfServer, portOfServer)
    print("starting up on %s port %s" % server_address)
    newSocket.bind(server_address)
    return newSocket