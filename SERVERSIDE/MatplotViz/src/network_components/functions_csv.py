import csv
from filelock import FileLock, Timeout

def initiateFileLock(filename):
    filelockname = filename+".lock"
    return FileLock(filelockname, timeout=1)

def initiateCSVFile(filename, filelock):
    headerRow = ["FRAME_ID","SF_ALLOC", "SF_PERIOD", "PERCENTAGE"]
    initialINDEX = appendNewRowToFile(filename, filelock, headerRow, "initialize")
    return initialINDEX    

def appendNewRowToFile(filename, filelock, newRowToAppend, writemode):
    filelock.acquire()
    INDEX = newRowToAppend[0]
    try:
        copyAndOverwriteValues(filename, newRowToAppend, writemode)
    finally:
        filelock.release()
        return determineNextIndex(INDEX, writemode)

def copyAndOverwriteValues(filename, newRowToAppend,writemode):
    data = copyOldValues(filename, writemode)   
    data.append(newRowToAppend)
    newValues = data
    overwriteOldValues(filename, newValues)

def copyOldValues(filename, writemode):
    data = []
    if writemode == "append":
        with open(filename, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            for row in csv_reader:
                data.append(row) 
    return data

def overwriteOldValues(filename, newValues):
    with open(filename, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(newValues)
    print("New row appended to file...")

def determineNextIndex(INDEX, writemode):
    if writemode == "append":
        return INDEX+1
    return 0  
