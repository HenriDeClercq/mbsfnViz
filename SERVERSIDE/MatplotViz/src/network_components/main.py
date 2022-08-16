import argparse
from server import Server

def main(addressOfServer, portOfServer, filename):
    listener = Server(addressOfServer, portOfServer, filename)
    listener.run()
    
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
