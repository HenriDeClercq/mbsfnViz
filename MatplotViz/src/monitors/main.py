import argparse
import type_bardiagram as bar
import type_piechart as pie

def main(monitorType, fileName, columnToPlot, horizontalWindowSize, sleepTime):
    if monitorType == "bardiagram":
        monitor = bar.Monitor(fileName, columnToPlot, horizontalWindowSize, sleepTime)
    elif monitorType == "piechart":
        monitor = pie.Monitor(fileName, columnToPlot, sleepTime)
    else:
        print("WRONG MONITORTYPE")
        return
    monitor.run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a type of Monitor')
    
    parser.add_argument('--monitorType', type=str, required=False, default= "bardiagram",
                        help='choose: "piechart" or "bardiagram"')
    parser.add_argument('--filename', type=str, required=False, default= "default.csv",
                        help='the path to the csv filename')
    parser.add_argument('--columnToPlot', type = str, required=False, default = "PERCENTAGE", 
                        help='choose: "SF_ALLOC" or "SF_PERIOD"')
    parser.add_argument('--horizontalWindowSize', type = int, required=False, default = 20,
                        help='the width of the window x axis')
    parser.add_argument('--sleepTime', type = float, required=False, default = 0.1,
                        help='time to sleep between frames')
    args = parser.parse_args()
    main(monitorType = args.monitorType, fileName=args.filename, columnToPlot=args.columnToPlot, horizontalWindowSize = args.horizontalWindowSize, sleepTime = args.sleepTime) 
