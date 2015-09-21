from IGA_analyse import IGA_Analyse
import simplejson as json 
from IGA_plot import IGA_Plot
import numpy as np


if __name__ == '__main__':
	analyse = IGA_Analyse()
	analyse.load()

	analyse.analyseAll()

	# print json.dumps({"blanks":analyse.blanks,"aliqs":analyse.aliqs}, sort_keys=True, indent=4, separators=(',', ': '))

	plot = IGA_Plot(analyse)
	plot.rawPlot()
	plot.alignedPlot()
	plot.rawDiffPlot()
	plot.alignedDiffPlot()
	plot.alignedAveragePlot()