#### Script for plotting machine produced data ####

#### TGA (machine 1) ####

import glob, os
from collections import OrderedDict, Counter
import simplejson as json 	
import matplotlib
import matplotlib.markers as mark
from matplotlib.markers import MarkerStyle
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import lines as plotline
from matplotlib.pyplot import show, plot, ion, figure
import pylab
import numpy as np
import random

# Fix pyplot imports.

#X 50
# Y 5


class AMC_Plot: 

	def __init__(self, analyse):
	 
		self.plotIni = "AMininstance"
		self.analyse = analyse

	def htmlcolor(self, r, g, b):
	    def _chkarg(a):
	        if isinstance(a, int): # clamp to range 0--255
	            if a < 0:
	                a = 0
	            elif a > 255:
	                a = 255
	        elif isinstance(a, float): # clamp to range 0.0--1.0 and convert to integer 0--255
	            if a < 0.0:
	                a = 0
	            elif a > 1.0:
	                a = 255
	            else:
	                a = int(round(a*255))
	        else:
	            raise ValueError('Arguments must be integers or floats.')
	        return a
	    r = _chkarg(r)
	    g = _chkarg(g)
	    b = _chkarg(b)
	    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

	def rawPlot(self):

		#Blank First
		for experiment in self.analyse.blanks:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["raw_runs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["ads"][0], run["ads"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Blank_%s_Ads_Run_%s'%(experiment["name"], run["sample"]))
			
			plt.axis([0, 45, 0, 0.35])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mg)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Many_plots/Adsorption/Raw_Runs_Ads_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["raw_runs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["des"][0], run["des"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Blank_%s_Des_Run_%s'%(experiment["name"], run["sample"]))
			
			plt.axis([0, 45, 0, 0.35])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mg)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Many_plots/Desorption/Raw_Runs_Des_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

		# Aliqs next
		for experiment in self.analyse.aliqs:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["raw_runs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["ads"][0], run["ads"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Aliq_%s_Ads_Run_%s'%(experiment["name"], run["sample"]))
			
			plt.axis([0, 50, 0, 5])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mmol/g)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Aliq_plots/Many_plots/Adsorption/Raw_Runs_Ads_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["raw_runs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["des"][0], run["des"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Aliq_%s_Des_Run_%s'%(experiment["name"], run["sample"]))
			
			plt.axis([0, 50, 0, 5])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mmol/g)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Aliq_plots/Many_plots/Desorption/Raw_Runs_Des_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

	def alignedPlot(self):

		#Blank First
		for experiment in self.analyse.blanks:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["aligned_runs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["ads"][0], run["ads"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Blank_%s_Ads_Run_%s'%(experiment["name"], run["sample"]))
			
			plt.axis([0, 50, 0, 0.35])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mg)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Many_plots/Adsorption/Aligned_Runs_Ads_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["aligned_runs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["des"][0], run["des"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Blank_%s_Des_Run_%s'%(experiment["name"], run["sample"]))
			
			plt.axis([0, 50, 0, 0.35])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mg)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Many_plots/Desorption/Aligned_Runs_Des_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

		# Aliqs next
		for experiment in self.analyse.aliqs:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["aligned_runs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["ads"][0], run["ads"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Aliq_%s_Ads_Run_%s'%(experiment["name"], run["sample"]))
			
			plt.axis([0, 50, 0, 5])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mmol/g)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Aliq_plots/Many_plots/Adsorption/Aligned_Runs_Ads_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["aligned_runs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["des"][0], run["des"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Aliq_%s_Des_Run_%s'%(experiment["name"], run["sample"]))
			
			plt.axis([0, 50, 0, 5])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mmol/g)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Aliq_plots/Many_plots/Desorption/Aligned_Runs_Des_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()


	def rawDiffPlot(self):

		#Blank First
		for experiment in self.analyse.blanks:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["raw_diffs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["ads"][0], run["ads"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Blank_%s_Ads_Diff_%s-%s'%(experiment["name"], run["i"], run["j"]))
			
			plt.axis([0, 45, 0, 0.02])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mg)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Diff_plots/Adsorption/Raw_Diffs_Ads_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["raw_diffs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["des"][0], run["des"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Blank_%s_Des_Diff_%s-%s'%(experiment["name"], run["i"], run["j"]))
			
			plt.axis([0, 45, 0, 0.3])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mg)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Diff_plots/Desorption/Raw_Diffs_Des_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

		# Aliqs next
		for experiment in self.analyse.aliqs:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["raw_diffs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["ads"][0], run["ads"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Aliq_%s_Ads_Diff_%s-%s'%(experiment["name"], run["i"], run["j"]))
			
			plt.axis([0, 45, 0, 0.3])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mmol/g)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Aliq_plots/Diff_plots/Adsorption/Raw_Diffs_Ads_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["raw_diffs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["des"][0], run["des"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Aliq_%s_Des_Diff_%s-%s'%(experiment["name"], run["i"], run["j"]))
			
			plt.axis([0, 45, 0, 0.3])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mmol/g)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Aliq_plots/Diff_plots/Desorption/Raw_Diffs_Des_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

	def alignedDiffPlot(self):

		#Blank First
		for experiment in self.analyse.blanks:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["aligned_diffs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["ads"][0], run["ads"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Blank_%s_Ads_Diff_%s-%s'%(experiment["name"], run["i"], run["j"]))
			
			plt.axis([0, 45, 0, 0.02])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mg)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Diff_plots/Adsorption/Aligned_Diffs_Ads_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["aligned_diffs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["des"][0], run["des"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Blank_%s_Des_Diff_%s-%s'%(experiment["name"], run["i"], run["j"]))
			
			plt.axis([0, 45, 0, 0.3])
			plt.xlabel('Pressure (Bar)')	
			plt.ylabel('Uptake (mg)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Diff_plots/Desorption/Aligned_Diffs_Des_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

		# Aliqs next
		for experiment in self.analyse.aliqs:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["aligned_diffs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["ads"][0], run["ads"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Aliq_%s_Ads_Diff_%s-%s'%(experiment["name"], run["i"], run["j"]))
			
			plt.axis([0, 45, 0, 0.3])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mmol/g)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Aliq_plots/Diff_plots/Adsorption/Aligned_Diffs_Ads_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			for run in experiment["aligned_diffs"]:
				self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
				plt.plot(run["des"][0], run["des"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
				legend.append('Aliq_%s_Des_Diff_%s-%s'%(experiment["name"], run["i"], run["j"]))
			
			plt.axis([0, 45, 0, 0.3])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mmol/g)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Aliq_plots/Diff_plots/Desorption/Aligned_Diffs_Des_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

	def alignedAveragePlot(self):

		#Blank First
		for experiment in self.analyse.blanks:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			run =  experiment["aligned_average"]

			self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
			plt.plot(run["ads"][0], run["ads"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
			legend.append('Blank_Ads_Average_%s-%s'%(experiment["name"], experiment["element"]))

			self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
			plt.plot(run["des"][0], run["des"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
			legend.append('Blank_Des_Average_%s-%s'%(experiment["name"], experiment["element"]))
			
			plt.axis([0, 45, 0, 0.3])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mg)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Simple_plots/Aligned_Average_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

		# Aliqs next
		for experiment in self.analyse.aliqs:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			legend = []
			run =  experiment["aligned_average"]

			self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
			plt.plot(run["ads"][0], run["ads"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
			legend.append('Aliq_Ads_Average_%s-%s'%(experiment["name"], experiment["element"]))

			self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
			plt.plot(run["des"][0], run["des"][1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
			legend.append('Aliq_Des_Average_%s-%s'%(experiment["name"], experiment["element"]))
			
			plt.axis([0, 45, 0, 0.3])
			plt.xlabel('Pressure (Bar)')
			plt.ylabel('Uptake (mmol/g)')
			plt.grid(b=True, which='major', color='k', linestyle='-')
			plt.legend(legend, loc = 2, fontsize = 10)

			self.ads_blankManyPath = '%s/AMC/AMC_plots/Aliq_plots/Simple_plots/Aligned_Average_plot_%s_%s.png'%(os.getcwd(), experiment["name"], experiment["element"])
			plt.savefig('%s'%self.ads_blankManyPath)
			plt.close()

######################################### Many_plot Functions #########################################

	def ads_aliqManyPlot(self, manyList, label='unknown', xmin = 0, ymin = 0, xmax = 45, ymax = 20):
		
		self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))

		fig = plt.figure()
		ax = fig.add_subplot(111)
		for num in manyList:
			# index = manyList.index(num)
			plt.plot(num[0], num[1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)

		plt.axis([xmin, xmax, ymin, ymax])
		plt.xlabel('Pressure (Bar)')
		plt.ylabel('Uptake (mmol/g)')
		plt.grid(b=True, which='major', color='k', linestyle='-')

		self.ads_aliqManyPath = '%s/AMC/AMC_plots/Aliq_plots/Many_plots/Adsorption/many_plot_%s.png'%(os.getcwd(), label)
		plt.savefig('%s'%self.ads_aliqManyPath)
		plt.close()

	def des_aliqManyPlot(self, manyList, label='unknown', xmin = 0, ymin = 0, xmax = 45, ymax = 20):
		
		self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))

		fig = plt.figure()
		ax = fig.add_subplot(111)
		for num in manyList:
			# index = manyList.index(num)
			plt.plot(num[0], num[1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
			# plt.legend(['Line Number: %s'%index], loc = 2)
		
		plt.axis([xmin, xmax, ymin, ymax])
		plt.xlabel('Pressure (Bar)')
		plt.ylabel('Uptake (mmol/g)')
		plt.grid(b=True, which='major', color='k', linestyle='-')

		self.des_aliqManyPath = '%s/AMC/AMC_plots/Aliq_plots/Many_plots/Desorption/many_plot_%s.png'%(os.getcwd(), label)
		plt.savefig('%s'%self.des_aliqManyPath)
		plt.close()

	def ads_blankManyPlot(self, manyList, label='unknown', xmin = 0, ymin = 0, xmax = 45, ymax = 1.2):
		
		self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))

		fig = plt.figure()
		ax = fig.add_subplot(111)
		for num in manyList:
			# index = manyList.index(num)
			plt.plot(num[0], num[1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
			# plt.legend(['Line Number: %s'%index], loc = 2)
		
		plt.axis([xmin, xmax, ymin, ymax])
		plt.xlabel('Pressure (Bar)')
		plt.ylabel('Uptake (mmol/g)')
		plt.grid(b=True, which='major', color='k', linestyle='-')

		self.ads_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Many_plots/Adsorption/many_plot_%s.png'%(os.getcwd(), label)
		plt.savefig('%s'%self.ads_blankManyPath)
		plt.close()

	def des_blankManyPlot(self, manyList, label='unknown', xmin = 0, ymin = 0, xmax = 45, ymax = 1.2):
		
		self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))

		fig = plt.figure()
		ax = fig.add_subplot(111)
		for num in manyList:
			index = manyList.index(num)
			plt.plot(num[0], num[1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
			# plt.legend(['Line Number: %s'%index], loc = 2)
		
		plt.axis([xmin, xmax, ymin, ymax])
		plt.xlabel('Pressure (Bar)')
		plt.ylabel('Uptake (mmol/g)')
		plt.grid(b=True, which='major', color='k', linestyle='-')

		self.des_blankManyPath = '%s/AMC/AMC_plots/Blank_plots/Many_plots/Desorption/many_plot_%s.png'%(os.getcwd(), label)
		plt.savefig('%s'%self.des_blankManyPath)
		plt.close()
	
######################################### Diff_plot Functions #########################################


	def des_blankDiffPlot(self, listOne, listTwo, listDiff, label='unkown', index=0,\
						  legendOne = 'unknown', legendTwo = 'unknown', legendDiff = 'unknown',\
						  xmin = 0, xmax = 45, ymin = 0, ymax = 0.5):

		self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
		self.color2 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
		self.color3 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))

		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.plot(listOne[0], listOne[1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		plt.plot(listTwo[0], listTwo[1], 'o', ms = float(5.0), color = self.color2, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		plt.plot(listDiff[0], listDiff[1], 'o', ms = float(5.0), color = self.color3, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		
		plt.grid(b=True, which='major', color='k', linestyle='-')
		plt.axis([xmin, xmax, ymin, ymax])
		plt.xlabel('Pressure (Bar)')
		plt.ylabel('Uptake (mmol/g)')
		plt.legend([legendOne, legendTwo, legendDiff], loc = 2, fontsize = 10)

		self.des_blankDiffPath = '%s/AMC/AMC_plots/Blank_plots/Diff_plots/Desorption/diff_plot_%s_%d.png'\
					 	 			  %(os.getcwd(), label, index)
		plt.savefig('%s'%self.des_blankDiffPath)	
		plt.close()			

	def ads_blankDiffPlot(self, listOne, listTwo, listDiff, label='unknown', index=0,\
						  legendOne = 'unknown', legendTwo = 'unknown', legendDiff = 'unknown',\
						  xmin = 0, xmax = 45, ymin = 0, ymax = 0.5):

		self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
		self.color2 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
		self.color3 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))

		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.plot(listOne[0], listOne[1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		plt.plot(listTwo[0], listTwo[1], 'o', ms = float(5.0), color = self.color2, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		plt.plot(listDiff[0], listDiff[1], 'o', ms = float(5.0), color = self.color3, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		
		plt.grid(b=True, which='major', color='k', linestyle='-')
		plt.axis([xmin, xmax, ymin, ymax])
		plt.xlabel('Pressure (Bar)')
		plt.ylabel('Uptake (Change in Mass (mg))')
		plt.legend([legendOne, legendTwo, legendDiff], loc = 2, fontsize = 10)

		self.ads_blankDiffPath = '%s/AMC/AMC_plots/Blank_plots/Diff_plots/Adsorption/diff_plot_%s_%d.png'\
					 	 			  %(os.getcwd(), label, index)
		plt.savefig('%s'%self.ads_blankDiffPath)
		plt.close()

	def des_aliqDiffPlot(self, listOne, listTwo, listDiff, label='unknown', index=0,\
						 legendOne = 'unknown', legendTwo = 'unknown', legendDiff = 'unknown',\
						  xmin = 0, xmax = 45, ymin = 0, ymax = 1.2):

		self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
		self.color2 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
		self.color3 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))

		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.plot(listOne[0], listOne[1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		plt.plot(listTwo[0], listTwo[1], 'o', ms = float(5.0), color = self.color2, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		plt.plot(listDiff[0], listDiff[1], 'o', ms = float(5.0), color = self.color3, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		
		plt.grid(b=True, which='major', color='k', linestyle='-')
		plt.axis([xmin, xmax, ymin, ymax])
		plt.xlabel('Pressure (Bar)')
		plt.ylabel('Uptake (mmol/g)')
		plt.legend([legendOne, legendTwo, legendDiff], loc = 2, fontsize = 10)

		self.des_aliqDiffPath = '%s/AMC/AMC_plots/Aliq_plots/Diff_plots/Desorption/diff_plot_%s_%d.png'\
					 	 			  %(os.getcwd(), label, index)
		plt.savefig('%s'%self.des_aliqDiffPath)	
		plt.close()			

	def ads_aliqDiffPlot(self, listOne, listTwo, listDiff, label='unknown', index=0,\
						 legendOne = 'unknown', legendTwo = 'unknown', legendDiff = 'unknown',\
						  xmin = 0, xmax = 45, ymin = 0, ymax = 1.2):

		self.color1 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
		self.color2 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
		self.color3 = self.htmlcolor(random.randint(0,255), random.randint(0,255), random.randint(0,255))

		fig = plt.figure()
		ax = fig.add_subplot(111)
		
		plt.plot(listOne[0], listOne[1], 'o', ms = float(5.0), color = self.color1, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		plt.plot(listTwo[0], listTwo[1], 'o', ms = float(5.0), color = self.color2, mew = .25, ls = '-', lw = float(1.5), zorder = 3)
		plt.plot(listDiff[0], listDiff[1], 'o', ms = float(5.0), color = self.color3, mew = .25, ls = '-', lw = float(1.5), zorder = 3)

		plt.grid(b=True, which='major', color='k', linestyle='-')
		plt.axis([xmin, xmax, ymin, ymax])
		plt.xlabel('Pressure (Bar)')
		plt.ylabel('Uptake (weight%)')
		plt.legend([legendOne, legendTwo, legendDiff], loc = 2, fontsize = 10)

		self.ads_aliqDiffPath = '%s/AMC/AMC_plots/Aliq_plots/Diff_plots/Adsorption/diff_plot_%s_%d.png'\
					 	 			  %(os.getcwd(), label, index)
		plt.savefig('%s'%self.ads_aliqDiffPath)
		plt.close()

######################################### Simple_plot Functions #########################################

	def aliqSimplePlot(self, listOne, listTwo, label='unknown', legendOne = 'unknown',\
					   legendTwo = 'unknown', xmin = 0, xmax = 45, ymin = 0, ymax = 20):
		fig = plt.figure()
		ax = fig.add_subplot(111)
		
		plt.plot(listOne[0], listOne[1], 'ro', mec = 'r', ms = float(4.5), ls = '-', lw = float(1.5), label = 'unknown', zorder = 3.5)
		plt.plot(listTwo[0], listTwo[1], 'bo', mec = 'b', ms = float(4.5), ls = '-', lw = float(1.5), label = 'unknown', zorder = 3.5)

		plt.grid(b=True, which='major', color='k', linestyle='-')
		plt.axis([xmin, xmax, ymin, ymax])
		plt.xlabel('Pressure (Bar)')
		plt.ylabel('Uptake (mmol/g)')
		plt.legend([legendOne, legendTwo], loc = 2, fontsize = 10)
		# plotline.Line2D(listOne[0], listOne[1], 'r', linestyle = '-')
		# plotline.Line2D(listTwo[0], listTwo[1], 'b', linestyle = '-')

		self.aliq_SimplePath = '%s/AMC/AMC_plots/Aliq_plots/Simple_plots/simple_plot_%s.png'\
					 	 		 %(os.getcwd(), label)
		plt.savefig('%s'%self.aliq_SimplePath)
		plt.close()

	def blankSimplePlot(self, listOne, listTwo, label='unknown', legendOne = 'unknown',\
					    legendTwo = 'unknown', xmin = 0, xmax = 45, ymin = 0, ymax = 1.2):
		fig = plt.figure()
		ax = fig.add_subplot(111)
		
		plt.plot(listOne[0], listOne[1], 'ro', mec = 'r', ms = float(4.5), ls = '-', lw = float(1.5), label = 'unknown', zorder = 3.5)
		plt.plot(listTwo[0], listTwo[1], 'bo', mec = 'b', ms = float(4.5), ls = '-', lw = float(1.5), label = 'unknown', zorder = 3.5)

		plt.grid(b=True, which='major', color='k', linestyle='-')
		plt.axis([xmin, xmax, ymin, ymax])
		plt.xlabel('Pressure (Bar)')
		plt.ylabel('Uptake (mmol/g)')
		plt.legend([legendOne, legendTwo], loc = 2, fontsize = 10)
		plotline.Line2D(listOne[0], listOne[1], 'r', linestyle = '-')
		plotline.Line2D(listTwo[0], listTwo[1], 'b', linestyle = '-')

		self.blank_SimplePath = '%s/AMC/AMC_plots/Blank_plots/Simple_plots/simple_plot_%s.png'\
					 	 		 %(os.getcwd(), label)
		plt.savefig('%s'%self.blank_SimplePath)
		plt.close()

