import pandas as pd
from pyparsing import col
from filelock import FileLock, Timeout
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Monitor:
    def __init__(self, fileName, columnToPlot, horizontalWindowSize):
            self.plotRefreshRate = 60
            self.filelock = FileLock(fileName+".lock", timeout=1)
            self.legal_SF_ALLOC_VALUES = [1,2,3,4,5,6]
            self.legal_SF_PERIOD_VALUES = [1,2,4,8,16,32]
            self.iteratorPosition = 0
            self.setCOLUMNINDEX(columnToPlot)
    	    # tweakable arguments
            self.fileName = fileName
            self.columnToPlot = columnToPlot
            self.horizontalWindowSize = horizontalWindowSize

    def run(self):
        animation = FuncAnimation(plt.gcf(), self.drawNextFrame, self.plotRefreshRate)
        plt.show()

    def readCSV(self):
        self.filelock.acquire()
        try:
            valuesOfAllColumns = pd.read_csv(self.fileName, skiprows = self.iteratorPosition, nrows = self.horizontalWindowSize)
            valuesOfXaxis = valuesOfAllColumns.iloc[:, 0]
            valuesOfDesiredColumn = valuesOfAllColumns.iloc[:, self.COLUMNINDEX]
            self.nextIteratorPosition(valuesOfAllColumns)
        finally:
            self.filelock.release()
        return valuesOfXaxis, valuesOfDesiredColumn

    def nextIteratorPosition(self, valuesOfAllColumns):
            if (valuesOfAllColumns.shape[0] == self.horizontalWindowSize):
                self.iteratorPosition+=1
    
    def setVisualPlotParameters(self):
        plt.cla()
        plt.title('File: ' + self.fileName.split("/")[-1])

    def fetchValuesToPlot(self):
        return self.readCSV()

    def getMaxLegalValue(self):
        if (self.columnToPlot == "SF_ALLOC"):
            maxValue = max(self.legal_SF_ALLOC_VALUES)
        if (self.columnToPlot == "SF_PERIOD"):
            maxValue = max(self.legal_SF_PERIOD_VALUES)
        return maxValue

    def setCOLUMNINDEX(self, columnToPlot):
        if columnToPlot == "SF_ALLOC":
            self.COLUMNINDEX = 1
        else:
            self.COLUMNINDEX = 2
    
    def drawNextFrame(self, i):
        print("Drawing next frame")