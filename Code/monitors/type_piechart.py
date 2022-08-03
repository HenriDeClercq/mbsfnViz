import matplotlib.pyplot as plt
from monitor import Monitor

class Monitor(Monitor):
    def __init__(self, fileName, columnToPlot):
            super().__init__(fileName, columnToPlot, 2)
            self.USEDFORMULTICAST, self.FREEFORUNICAST = "red", "green"
            
    def drawNextFrame(self, i):
        super().drawNextFrame(i)
        super().setVisualPlotParameters()
        valuesOfPiePieces, lablesOfPiePieces, colorsOfPiePieces = self.fetchValuesToPlot()
        plt.pie(valuesOfPiePieces, labels=lablesOfPiePieces, colors=colorsOfPiePieces)

    def fetchValuesToPlot(self):
        valuesOfXaxis, valuesOfDesiredColumn = super().fetchValuesToPlot()
        lastValueOfDesiredColumn = self.determineLastValueOfDesiredColumn(valuesOfDesiredColumn)
        valuesOfPiePieces = [self.determinePercentageUsedForMultiCast(lastValueOfDesiredColumn), self.determinePercentageFreeForUniCast(lastValueOfDesiredColumn)]
        labelsOfPiePieces = ["Used: " + str(round(100*valuesOfPiePieces[0],2)) + "%", "Free: " + str(round(100*valuesOfPiePieces[1],2)) + "%"] 
        colorsOfPiePieces =  [self.USEDFORMULTICAST, self.FREEFORUNICAST]
        return valuesOfPiePieces, labelsOfPiePieces, colorsOfPiePieces

    def determineLastValueOfDesiredColumn(self, allValuesOfDesiredColumn):
        lastValueOfDesiredColumn = allValuesOfDesiredColumn.tail(1).item()
        return lastValueOfDesiredColumn
 
    def determinePercentageUsedForMultiCast(self, lastValueOfDesiredColumn):
        maxLegalValue = self.getMaxLegalValue()
        return lastValueOfDesiredColumn/maxLegalValue

    def determinePercentageFreeForUniCast(self, lastValueOfDesiredColumn):
        maxLegalValue = super().getMaxLegalValue()
        return (maxLegalValue-lastValueOfDesiredColumn)/maxLegalValue