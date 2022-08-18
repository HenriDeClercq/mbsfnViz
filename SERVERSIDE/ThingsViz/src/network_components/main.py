import argparse
from server import Server

def main(addressOfBroker, portOfBroker, deviceAccessToken, topicGroup, addressOfServer, portOfServer):
    listener = Server(addressOfBroker, portOfBroker, deviceAccessToken, topicGroup, addressOfServer, portOfServer)
    listener.run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a random data generator client')
    parser.add_argument('--addressOfBroker', type=str, required=False, default= "localhost",
                        help='address of the broker => localhost or thingsboard.cloud')              
    parser.add_argument('--portOfBroker', type=int, required=False, default= 1883,
                        help='port of the broker')
    parser.add_argument('--deviceAccessToken, can be found in the devices tab of Thingsboard', type=str, required=False, default= "CGO0qUUI1BiPOkUhkYy7",
                        help='device access token of the device')
    parser.add_argument('--topicGroup', type=str, required=False, default= "ThingsViz/telemetry",
                        help='topic to publish on, can be found in the devices profile tab on Thingsboard')
    parser.add_argument('--addressOfServer', type=str, required=False, default= "localhost",
                        help='address of serversocket')
    parser.add_argument('--portOfServer', type=int, required=False, default= 10000,
                        help='port of serversocket')
    args = parser.parse_args()
    main(addressOfBroker = args.addressOfBroker, portOfBroker = args.portOfBroker, deviceAccessToken = args.deviceAccessToken, topicGroup = args.topicGroup, addressOfServer = args.addressOfServer, portOfServer = args.portOfServer)
