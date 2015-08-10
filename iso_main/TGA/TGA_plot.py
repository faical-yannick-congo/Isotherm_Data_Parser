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


class TGA_Plot: 

	def __init__(self):
	 
		self.plotIni = "TGininstance"

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
		plt.ylabel('Uptake (\delta Mass (mg)')
		plt.grid(b=True, which='major', color='k', linestyle='-')

		self.ads_aliqManyPath = '%s/TGA/TGA_plots/Aliq_plots/Many_plots/Adsorption/many_plot_%s.png'%(os.getcwd(), label)
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
		plt.ylabel('Uptake (\delta Mass (mg)')
		plt.grid(b=True, which='major', color='k', linestyle='-')

		self.des_aliqManyPath = '%s/TGA/TGA_plots/Aliq_plots/Many_plots/Desorption/many_plot_%s.png'%(os.getcwd(), label)
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
		plt.ylabel('Uptake (\delta Mass (mg)')
		plt.grid(b=True, which='major', color='k', linestyle='-')

		self.ads_blankManyPath = '%s/TGA/TGA_plots/Blank_plots/Many_plots/Adsorption/many_plot_%s.png'%(os.getcwd(), label)
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
		plt.ylabel('Uptake (\delta Mass (mg)')
		plt.grid(b=True, which='major', color='k', linestyle='-')

		self.des_blankManyPath = '%s/TGA/TGA_plots/Blank_plots/Many_plots/Desorption/many_plot_%s.png'%(os.getcwd(), label)
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
		plt.ylabel('Uptake (\delta Mass (mg)')
		plt.legend([legendOne, legendTwo, legendDiff], loc = 2, fontsize = 10)

		self.des_blankDiffPath = '%s/TGA/TGA_plots/Blank_plots/Diff_plots/Desorption/diff_plot_%s_%d.png'\
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

		self.ads_blankDiffPath = '%s/TGA/TGA_plots/Blank_plots/Diff_plots/Adsorption/diff_plot_%s_%d.png'\
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
		plt.ylabel('Uptake (\delta Mass (mg)')
		plt.legend([legendOne, legendTwo, legendDiff], loc = 2, fontsize = 10)

		self.des_aliqDiffPath = '%s/TGA/TGA_plots/Aliq_plots/Diff_plots/Desorption/diff_plot_%s_%d.png'\
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

		self.ads_aliqDiffPath = '%s/TGA/TGA_plots/Aliq_plots/Diff_plots/Adsorption/diff_plot_%s_%d.png'\
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
		plt.ylabel('Uptake (\delta Mass (mg)')
		plt.legend([legendOne, legendTwo], loc = 2, fontsize = 10)
		# plotline.Line2D(listOne[0], listOne[1], 'r', linestyle = '-')
		# plotline.Line2D(listTwo[0], listTwo[1], 'b', linestyle = '-')

		self.aliq_SimplePath = '%s/TGA/TGA_plots/Aliq_plots/Simple_plots/simple_plot_%s.png'\
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
		plt.ylabel('Uptake (\delta Mass (mg)')
		plt.legend([legendOne, legendTwo], loc = 2, fontsize = 10)
		plotline.Line2D(listOne[0], listOne[1], 'r', linestyle = '-')
		plotline.Line2D(listTwo[0], listTwo[1], 'b', linestyle = '-')

		self.blank_SimplePath = '%s/TGA/TGA_plots/Blank_plots/Simple_plots/simple_plot_%s.png'\
					 	 		 %(os.getcwd(), label)
		plt.savefig('%s'%self.blank_SimplePath)
		plt.close()

#self.adsBlankIndivList = self.adsBlankMainList[firstNum]

# 		self.adsBlankPresVals = self.adsBlankIndivList[0]
# 		self.adsBlankConcVals = self.adsBlankIndivList[1]

# 		self.desBlankIndivList = self.desBlankMainList[firstNum]

# 		self.desBlankPresVals = self.desBlankPresList[0]
# 		self.desBlankConcVals = self.desBlankConcList[1]

	
# 	def plotSimpleAliq(self):
# 		plt.figure(indexAliq)
# 		plt.plot(self.adsAliqPresVals, self.adsAliqConcVals, mfc = 'r', mew = .25)
# 		plt.plot(self.desAliqPresVals, self.desAliqConcVals, mfc = 'b', mew = .25)
	
# 		plot_AliqPath = '%s/TGA/TGA_plots/Aliq_plots/Simple_plots/%s_simplePlot_%s.png'\
# 							 %(os.getcwd(), sequence1, indexAliq)
# 		plt.savefig('%s'%plot_simplePath)


# 	def plotSimpleBlank(self):
# 		plt.figure(indexBlank)
# 		plt.plot(self.adsPresVals, self.adsConcVals, mfc = 'r', mew = .25)
# 		plt.plot(self.desPresVals, self.desConcVals,  mfc = 'b', mew = .25)
	
# 		plot_blankPath = '%s/TGA/TGA_plots/Blank_plots/Simple_plots/%s_simplePlot_%s.png'\
# 							 %(os.getcwd(), sequence1, indexBlank)
# 		plt.savefig('%s'%plot_blankPath)

# 		start2 += 1
# 		indexBlank += 1

# class multiPlotsTGA	

# 	def plotMany(self):


# if __name__ == '__main__':

# 	os.chdir(os.path.dirname(os.getcwd()))

# 	start1 = 0
# 	start2 = 0
# 	indexBlank = 1
# 	indexAliq = 1

# 	while True:
# 		try:
# 			for file in glob.glob("TGA/Data_Files/JSON/json_aliq/*.json"):
# 				sequence1 = file.split("/")[-1].split("_")[0]
# 				sequence2 = file.split("/")[-1].split("_")[1]
# 				sequence3 = file.split("/")[-1].split("_")[2]

# 				json_aliqPathTGA = file

# 				with open('%s'%json_aliqPathTGA) as json_aliqDataTGA:    
# 					json_aliqDictTGA = json.load(json_aliqDataTGA)


# 				begin3 = 1

# 				pressureAliq_listTGA = []
# 				concAliq_listTGA = []


# 				while True: 
# 					try:
# 						contentAliq_dictTGA = json_AliqDictTGA["content"][begin3 - 1]

# 						concAliq_dictTGA = contentAliq_dictTGA.get('weights')[4]
# 						concAliq_valTGA = concAliq_dictTGA.get('value')

# 						pressureAliq_dictTGA = contentAliq_dictTGA.get('pressure')
# 						pressureAliq_valTGA = pressureAliq_dictTGA.get('value')

# 						pressureAliq_listTGA.append(pressure_valTGA)
# 						concAliq_listTGA.append(conc_valTGA)
						
# 						begin3 +=1

# 					except:
# 						break


# 				total = len(pressureAliq_listTGA)

# 				pressureAliq_listTGA1 = []
# 				concAliq_listTGA1 = []

# 				pressureAliq_listTGA2 = []
# 				concAliq_listTGA2 = []
			
# 				boundary = -1
# 				for t in range(total):
# 					if t == total - 1:
# 						break
# 					elif t > 0:
# 						if pressureAliq_listTGA[t] >= pressureAliq_listTGA[t + 1] and pressureAliq_listTGA[t] >= pressureAliq_listTGA[t - 1]:
# 							boundary = t
# 							break
# 						if pressureAliq_listTGA[t] <= pressureAliq_listTGA[t + 1] and pressureAliq_listTGA[t] <= pressureAliq_listTGA[t - 1]:
# 							boundary = t
# 							break

# 				pressureAliq_listTGA1 = list(pressureAliq_listTGA[0:boundary])
# 				pressureAliq_listTGA2 = list(pressureAliq_listTGA[boundary + 1:len(pressureAliq_listTGA) - 1])

# 				concAliq_listTGA1 = list(concAliq_listTGA[0:boundary])
# 				concAliq_listTGA2 = list(concAliq_listTGA[boundary + 1:len(concAliq_listTGA) - 1])
			
# 				TGhay = simplePlotsTGA()
# 				TGhay.root.mainloop()
# 				self.root.mainloop()
			
# 				self.root.destroy()

# 				start1 += 1
# 				indexAliq += 1

# 		except:
# 			for file in glob.glob("TGA/Data_Files/JSON/json_blankRuns/*.json"):
# 				sequence1 = file.split("/")[-1].split("_")[0]
# 				sequence2 = file.split("/")[-1].split("_")[1]
# 				sequence3 = file.split("/")[-1].split("_")[2]

# 				json_blankPathTGA = file

# 				with open('%s'%json_blankPathTGA) as json_blankDataTGA:    
# 					json_blankDictTGA = json.load(json_blankDataTGA)


# 				begin4 = 1

# 				pressureBlank_listTGA = []
# 				concBlank_listTGA = []


# 				while True: 
# 					try:
# 						contentBlank_dictTGA = json_BlankDictTGA["content"][begin4 - 1]

# 						concBlank_dictTGA = contentBlank_dictTGA.get('weights')[4]
# 						concBlank_valTGA = concBlank_dictTGA.get('value')

# 						pressureBlank_dictTGA = contentBlank_dictTGA.get('pressure')
# 						pressureBlank_valTGA = pressureBlank_dictTGA.get('value')

# 						pressureBlank_listTGA.append(pressureBlank_valTGA)
# 						concBlank_listTGA.append(concBlank_valTGA)
						
# 						begin4 +=1

# 					except:
# 						break


# 				total = len(pressureBlank_listTGA)

# 				pressureBlank_listTGA1 = []
# 				concBlank_listTGA1 = []

# 				pressureBlank_listTGA2 = []
# 				concBlank_listTGA2 = []
			
# 				boundary = -1
# 				for t in range(total):
# 					if t == total - 1:
# 						break
# 					elif t > 0:
# 						if pressureBlank_listTGA[t] >= pressureBlank_listTGA[t + 1] and pressureBlank_listTGA[t] >= pressureBlank_listTGA[t - 1]:
# 							boundary = t
# 							break
# 						if pressureBlank_listTGA[t] <= pressureBlank_listTGA[t + 1] and pressureBlank_listTGA[t] <= pressureBlank_listTGA[t - 1]:
# 							boundary = t
# 							break

# 				pressureBlank_listTGA1 = list(pressureBlank_listTGA[0:boundary])
# 				pressureBlank_listTGA2 = list(pressureBlank_listTGA[boundary + 1:len(pressureBlank_listTGA) - 1])

# 				concBlank_listTGA1 = list(concBlank_listTGA[0:boundary])
# 				concBlank_listTGA2 = list(concBlank_listTGA[boundary + 1:len(concBlank_listTGA) - 1])
			
# 				TGhay = simplePlotsTGA()
# 				TGhay.root.mainloop()
# 				self.root.mainloop()
			
# 				self.root.destroy()

# 				start2 += 1
# 				indexBlank += 1
		




