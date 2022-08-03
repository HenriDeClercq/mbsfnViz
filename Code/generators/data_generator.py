import csv
import time
import random
import argparse
from filelock import FileLock, Timeout

class dataGenerator:
    def __init__(self, sleeptime, filename = "csv_files/random_generated.csv"):
        self.filename = filename
        self.filelockname = filename+".lock"
        self.filelock = FileLock(self.filelockname, timeout=1)
        self.INDEX = 0

        self.sleeptime = sleeptime
        self.legal_SF_ALLOC = [1,2,3,4,5,6]
        self.legal_SF_PERIOD = [1,2,4,8,16,32]
        self.legal_WRITEMODES = ["initialize", "append"]
        self.appendNewRowToFile(["FRAME_ID","SF_ALLOC", "SF_PERIOD"], "initialize")
        
    def run(self):
        while True:
            SF_ALLOC, SF_PERIOD = self.generateNewRandomFrame()
            newRowToAppend = [self.INDEX, SF_ALLOC, SF_PERIOD]
            self.appendNewRowToFile(newRowToAppend, "append")
            time.sleep(self.sleeptime)

    def appendNewRowToFile(self, newRowToAppend, writemode):
        self.filelock.acquire()
        try:
            self.checkIfLegalWriteMode(writemode)
            data = self.copyOldDataValues(writemode)     
            data.append(newRowToAppend)
            self.overwriteOldFileValues(data)
        finally:
            self.filelock.release()

    def generateNewRandomFrame(self):
            self.INDEX += 1
            SF_ALLOC = random.choice(self.legal_SF_ALLOC)
            SF_PERIOD = random.choice(self.legal_SF_PERIOD)
            return (SF_ALLOC, SF_PERIOD)

    def checkIfLegalWriteMode(self, writemode):
        if not (writemode in self.legal_WRITEMODES):
            print("ILLEGAL WRITEMODE")

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
    
def main(sleeptime):
    generator = dataGenerator(sleeptime)
    generator.run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a random data generator')
    parser.add_argument('--sleeptime', type=float, required=False, default= 0.5,
                        help='time between adding new rowes')
    args = parser.parse_args()
    main(sleeptime = args.sleeptime)

