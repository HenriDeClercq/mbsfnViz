#import pandas as pd
import matplotlib.pyplot as plt
from monitor import Monitor

class Monitor(Monitor):
    def __init__(self, fileName, columnToPlot, horizontalWindowSize, sleepTime):
            super().__init__(fileName, columnToPlot, horizontalWindowSize, sleepTime)
            self.BAR_WIDTH = 1

    def drawNextFrame(self, i):
        super().drawNextFrame(i)
        x_valuesOfBars, heightOfBars = self.fetchValuesToPlot()
        self.setVisualPlotParameters(x_valuesOfBars)
        plt.bar(x_valuesOfBars, heightOfBars, self.BAR_WIDTH, align = "edge", edgecolor = "black", color = "green")

    def fetchValuesToPlot(self):
        x_valuesOfBars, heightOfBars = super().fetchValuesToPlot()
        return x_valuesOfBars, heightOfBars

    def setVisualPlotParameters(self, x_valuesOfBars):
        super().setVisualPlotParameters()
        self.configure_Xaxis(x_valuesOfBars)
        self.configure_Yaxis()

    def configure_Xaxis(self, x_valuesOfBars):
        plt.xlabel("Frames")
        plt.xticks(x_valuesOfBars)

    def configure_Yaxis(self):
        if self.columnToPlot == "SF_ALLOC":
            plt.ylabel("sf alloc")
            plt.ylim([0,10])
        if self.columnToPlot == "SF_PERIOD":
            plt.ylabel("sf period")
            plt.ylim([1,32.6])
            plt.yticks(self.legal_SF_PERIOD_VALUES)
        if self.columnToPlot == "PERCENTAGE":
            plt.ylabel("percentage")
            plt.ylim([0,100])