import argparse
from server import Server

def main(addressOfBroker, portOfBroker, deviceAccessToken, topicGroup, addressOfServer, portOfServer, sleeptime):
    generator = Server(addressOfBroker, portOfBroker, deviceAccessToken, topicGroup, addressOfServer, portOfServer, sleeptime)
    generator.run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a random data generator client')
    parser.add_argument('--addressOfBroker', type=str, required=False, default= "localhost",
                        help='address of the broker')              
    parser.add_argument('--portOfBroker', type=int, required=False, default= 1883,
                        help='port of the broker')
    parser.add_argument('--deviceAccessToken', type=str, required=False, default= "pastedeviceaccesstokenhere",
                        help='device access token of the device')
    parser.add_argument('--topicGroup', type=str, required=False, default= "ThingsViz/telemetry",
                        help='topic to publish on')
    parser.add_argument('--addressOfServer', type=str, required=False, default= "localhost",
                        help='address of serversocket')
    parser.add_argument('--portOfServer', type=int, required=False, default= 10000,
                        help='port of serversocket')
    parser.add_argument('--sleeptime', type=float, required=False, default= 0.64,
                        help='time between sending new rowes')
    args = parser.parse_args()
    main(addressOfBroker = args.addressOfBroker, portOfBroker = args.portOfBroker, deviceAccessToken = args.deviceAccessToken, topicGroup = args.topicGroup, addressOfServer = args.addressOfServer, portOfServer = args.portOfServer, sleeptime = args.sleeptime)
