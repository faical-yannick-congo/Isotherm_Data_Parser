from AMC_analyse import AMC_Analyse
import simplejson as json 
from AMC_plot import AMC_Plot
import numpy as np


if __name__ == '__main__':
	analyse = AMC_Analyse()
	analyse.load()

	analyse.analyseAll()

	# print json.dumps({"blanks":analyse.blanks,"aliqs":analyse.aliqs}, sort_keys=True, indent=4, separators=(',', ': '))

	plot = AMC_Plot(analyse)
	plot.rawPlot()
	plot.alignedPlot()
	plot.rawDiffPlot()
	plot.alignedDiffPlot()
	plot.alignedAveragePlot()