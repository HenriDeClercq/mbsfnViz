import argparse
import type_bardiagram as bar
import type_piechart as pie

def main(monitorType, fileName, columnToPlot, horizontalWindowSize):
    if monitorType == "bardiagram":
        monitor = bar.Monitor(fileName, columnToPlot, horizontalWindowSize)
    elif monitorType == "piechart":
        monitor = pie.Monitor(fileName, columnToPlot)
    else:
        print("WRONG MONITORTYPE")
        return
    monitor.run()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a type of Monitor')
    
    parser.add_argument('--monitorType', type=str, required=False, default= "bardiagram",
                        help='choose: "piechart" or "bardiagram"')
    parser.add_argument('--fileName', type=str, required=False, default= "csv_files/random_generated.csv",
                        help='the path to the csv filename')
    parser.add_argument('--columnToPlot', type = str, required=False, default = "SF_ALLOC", 
                        help='choose: "SF_ALLOC" or "SF_PERIOD"')
    parser.add_argument('--horizontalWindowSize', type = int, required=False, default = 20,
                        help='the width of the window x axis')
    args = parser.parse_args()
    main(monitorType = args.monitorType, fileName=args.fileName, columnToPlot=args.columnToPlot, horizontalWindowSize = args.horizontalWindowSize)