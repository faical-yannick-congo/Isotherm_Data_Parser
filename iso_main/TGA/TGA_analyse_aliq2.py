import numpy as np
import glob, os
import simplejson as json 
import re

class TGA_AnalyseAliq2:
	def __init__(self):

		self.ADSmaster_list_blankCorr = []
		self.ADSmaster_list_raw = []

		self.DESmaster_list_blankCorr = []
		self.DESmaster_list_raw = []

		self.ADS_aliqMain = []
		self.DES_aliqMain = []

		self.origin_blanks = []
		self.origin_aliqs = []

		# blanks data
		self.ads_blank = []
		self.des_blank = []

		# aliqs data
		self.ads_aliq = []
		self.des_aliq = []

		# diff blanks data
		self.diff_ads_blank = []
		self.diff_des_blank = []
		self.diff_ads_blank = []
		self.diff_des_blank = []

		# diff aliqs data
		self.diff_ads_aliq = []
		self.diff_des_aliq = []
		self.diff_ads_aliq2 = []
		self.diff_des_aliq2 = []

		# average blanks data
		self.average_ads_blank = []
		self.average_des_blank = []
		
		# average aliqs data
		self.average_ads_aliq = []
		self.average_des_aliq = []

		# average diffs blanks data
		self.average_diff_ads_blank = []
		self.average_diff_des_blank = []

		# average diffs aliqs data
		self.average_diff_ads_aliq = []
		self.average_diff_des_aliq = []

		# corrected aliqs
		self.corrected_ads_aliq = []
		self.corrected_des_aliq = []

		# corrected average aliqs data
		self.average_corrected_ads_aliq = []
		self.average_corrected_des_aliq = []


	def load(self):
		# blanks = []
		# alisqs = []
		os.chdir(os.path.dirname(os.getcwd()))
		

		index = 0
		for file in glob.glob("TGA/Data_Files/JSON/json_aliq/*.json"):
			aliqPart = file.split("/")[-1]
			find_aliq = re.search('Aliq2', aliqPart)
				
			if find_aliq:
				content = None
				with open(file, "r") as aliq_file:
					content = aliq_file.read()
					raw = json.loads(content)
					# alisqs.append(raw)
					blocks = self.split(raw, run = 0)
					
					self.ads_aliq.append(blocks[0])
					self.des_aliq.append(blocks[1])
					filePart = file.split("/")[-1].split("_")[:4]
					
					aliqLabel = '_'.join(filePart)
					self.origin_aliqs.append(aliqLabel)

					index += 1
					
		# os.chdir(os.path.dirname(os.getcwd()))
		index = 0
		for file in glob.glob("TGA/Data_Files/JSON/json_blank/*.json"):
			content = None
			with open(file, "r") as blank_file:
				content = blank_file.read()

				raw = json.loads(content)
				# blanks.append(raw)
				blocks = self.split(raw, run = 0)
				self.ads_blank.append(blocks[0])
				self.des_blank.append(blocks[1])
				filePart = file.split("/")[-1].split("_")[:4]
				
				blankLabel = '_'.join(filePart)
				self.origin_blanks.append(blankLabel)
				
				index += 1

	def split(self, raw, run):

		begin3 = 1

		pressure_list = []
		conc_list = []

		
		while True: 
			try:
				content= raw["content"][begin3 - 1]				

				if run == 0: 
					conc_dict = content.get('weights')[3] # Before it was 3 but corrected to 4th and now second	
				elif run == 1:
					conc_dict = content.get('weights')[4]
				elif run == 2:
					conc_dict = content.get('weights')[2]

				conc_val = conc_dict.get('value')

				pressure_dict = content.get('pressure')
				pressure_val = pressure_dict.get('value')

				pressure_list.append(pressure_val)
				conc_list.append(conc_val)
					
				begin3 +=1

			except:
				break

		total = len(pressure_list) + 1

		corr_pres_index = pressure_list.index(max(pressure_list))
		corr_conc_value = conc_list[corr_pres_index]

		pressure_list1 = []
		conc_list1 = []

		pressure_list2 = []
		conc_list2 = []
		
		boundary = -1
		for t in range(total):
			if t == total - 1:
				break
			elif t > 0:
				if pressure_list[t] >= pressure_list[t + 1] and pressure_list[t] >= pressure_list[t - 1]:
					boundary = t
					break
				if pressure_list[t] <= pressure_list[t + 1] and pressure_list[t] <= pressure_list[t - 1]:
					boundary = t
					break

		pressure_list1 = list(pressure_list[0:boundary])
		pressure_list2 = list(pressure_list[boundary + 1:len(pressure_list) - 1])

		conc_list1 = list(conc_list[0:boundary])
		conc_list2 = list(conc_list[boundary + 1:len(conc_list) - 1])

		if max(pressure_list1) != max(pressure_list):  
			pressure_list1.append(max(pressure_list))
			conc_list1.append(corr_conc_value)

		return [[pressure_list1, conc_list1], [pressure_list2, conc_list2]]

	# x array to interpolate
	# The sampling.
	def align(self, dataX, dataXY, reverse=False):
		# print "dataX+++++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(dataX)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++++dataX"

		# print "dataXY+++++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(dataXY)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++++dataXY"

		self.UNDEF = -99.0

		if reverse:
			self.aligned = list(reversed(np.interp(list(reversed(dataX)), list(reversed(dataXY[0])), list(reversed(dataXY[1])))))
			
		else:
			self.aligned = list(np.interp(dataX, dataXY[0], dataXY[1]))
		
		# print "self.aligned++++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.aligned)
		# print "++++++++++++++++++++++++++++++++++++++++++++++++self.aligned"

		return self.aligned

	def diff(self, dataY1, dataY2):
		dataSub = np.array(dataY1) - np.array(dataY2)
		return [abs(data) for data in list(dataSub)]

	def average(self, dataY):
		# print "dataY+++++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(dataY)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++++dataY"
		averageY = [0.00 for d in dataY[0]]
		for data in dataY:
			for index in range(len(data)):
				averageY[index] += data[index]

		average = [float(d/len(averageY)) for d in averageY]

		# print "average+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(len(averageY) - 1)
		# print json.dumps(averageY)
		# print json.dumps(average)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average"

		return average


	def analyseBlank(self):
		##
		## self.average_DES_blank, self.average_des_blank, self.diff_DES_blank, self.diff_des_blank
		##
		#Total Average computations
		#Asbsorption align
	
		refPressure = None
		self.aligned_ads_blank = []
		
		#Determine the reference
		if len(self.ads_blank) > 0:
			refPressure = []
			for index in range(len(self.ads_blank[0][0])):
				value = [val[0][index] for val in self.ads_blank]
				avg_value = sum(value)/len(self.ads_blank)
				refPressure.append(avg_value)
		
		#Align all the rest
		for index in range(len(self.ads_blank)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.ads_blank[index]))
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			self.aligned_ads_blank.append([refPressure, x1])


		# self.aligned_average = []
		# for index in range(len(self.aligned_DES_blank[0][1])):
		# 	value = [val[1][index] for val in self.aligned_DES_blank]
		# 	avg_value = sum(value)/len(self.aligned_DES_blank)
		# 	self.aligned_average.append(avg_value)
		
		# self.average_DES_blank = [refPressure, self.aligned_average]

		#Desorbtion align
		refPressure = None
		self.aligned_des_blank = []
		
		#Determine the reference
		if len(self.des_blank) > 0:
			refPressure = []
			for index in range(len(self.des_blank[0][0])):
				value = [val[0][index] for val in self.des_blank]
				avg_value = sum(value)/len(self.des_blank)
				refPressure.append(avg_value)
		
		#Align all the rest
		for index in range(len(self.des_blank)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.des_blank[index], True))
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			self.aligned_des_blank.append([refPressure, x1])
		
		

		# self.aligned_average = []
		# for index in range(len(self.aligned_des_blank[0][1])):
		# 	value = [val[1][index] for val in self.aligned_des_blank]
		# 	avg_value = sum(value)/len(self.aligned_des_blank)
		# 	self.aligned_average.append(avg_value)
		
		# self.average_des_blank = [refPressure, self.aligned_average]

		##
		#Comabinatorial diff computations

		line = [0 for x in xrange(len(self.ads_blank))]
		already = [line[:] for x in xrange(len(self.ads_blank))]

		for indexI in range(0, len(self.ads_blank)):
			for indexJ in range(0, len(self.ads_blank)):

				if indexI == indexJ:
					# Do not compute same element case
					already[indexI][indexJ] = 0
					already[indexJ][indexI] = 0
				else:
					if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
					# Leave asymetric stuff for now. Later we could use it to average
					# for better approximation??? More dig is needed.
						already[indexJ][indexI] = 0
						already[indexI][indexJ] = 0
					else:
			
						# print x2
						interpolateK = self.align(self.ads_blank[indexJ][0], self.ads_blank[indexI])
						diffJK = self.diff(self.ads_blank[indexJ][1], interpolateK)
						
						
						d = diffJK
						upperQR = np.percentile(d, 75, interpolation='higher')
						lowerQR = np.percentile(d, 25, interpolation='lower')
						innerQR = upperQR - lowerQR
						limit = upperQR + (6*innerQR)

						problem = False
						for el in diffJK:
							if el > limit:
								problem = True

						if not problem:
							self.diff_ads_blank.append({'i':indexI, 'j':indexJ, 'diff':[self.ads_blank[indexJ][0], diffJK]})
		
	
		# print "diff_DES_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_DES_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_DES_blank"

		line = [0 for x in xrange(len(self.des_blank))]
		already = [line[:] for x in xrange(len(self.des_blank))]

		for indexI in range(0, len(self.des_blank)):
			for indexJ in range(0, len(self.des_blank)):

				if indexI == indexJ:
					# Do not compute same element case
					already[indexI][indexJ] = 0
					already[indexJ][indexI] = 0
				else:
					if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
					# Leave asymetric stuff for now. Later we could use it to average
					# for better approximation??? More dig is needed.
						already[indexJ][indexI] = 0
						already[indexI][indexJ] = 0
					else:
						# Computing self.des_blank[indexI] - self.des_blank[indexJ]
						# self.des_blank[indexJ] as to be self.aligned.

						interpolateK = self.align(self.des_blank[indexJ][0], self.des_blank[indexI], True)
						diffJK = self.diff(self.des_blank[indexJ][1], interpolateK)

						d = diffJK
						upperQR = np.percentile(d, 75, interpolation='higher')
						lowerQR = np.percentile(d, 25, interpolation='lower')
						innerQR = upperQR - lowerQR
						limit = upperQR + (6*innerQR)

						problem = False
						for el in diffJK:
							if el > limit:
								problem = True

						if not problem:
							self.diff_des_blank.append({'i':indexI, 'j':indexJ, 'diff':[self.des_blank[indexJ][0], diffJK]})		

		# print "diff_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_des_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_des_blank"
		
		
		##
		#Average diff computations
		#Asbsorption align
		refPressure = None
		self.aligned_ads_blank = []

		#Determine the reference
		if len(self.diff_ads_blank) > 0:
			refPressure = []
			for index in range(len(self.diff_ads_blank[0]['diff'][0])):
				value = [val['diff'][0][index] for val in self.diff_ads_blank]
				avg_value = sum(value)/len(self.diff_ads_blank)
				refPressure.append(avg_value)

		#Align all the rest
		for index in range(len(self.diff_ads_blank)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.diff_ads_blank[index]['diff']))
			self.aligned_ads_blank.append([refPressure, x1])

		self.aligned_average = []
		for index in range(len(self.aligned_ads_blank[0][1])):
			value = [val[1][index] for val in self.aligned_ads_blank]
			avg_value = sum(value)/len(self.aligned_ads_blank)
			self.aligned_average.append(avg_value)
		
		self.average_diff_ads_blank = [refPressure, self.aligned_average]

		# print self.average_diff_DES_blank

#######################################################################################
#######################################################################################

		#Desorbtion align
		refPressure= None
		self.aligned_des_blank = []

		#Determine the reference
		if len(self.diff_des_blank) > 0:
			refPressure = []
			for index in range(len(self.diff_des_blank[0]['diff'][0])):
				value = [val['diff'][0][index] for val in self.diff_des_blank]
				avg_value = sum(value)/len(self.diff_des_blank)
				refPressure.append(avg_value)
			
		#Align all the rest
		for index in range(len(self.diff_des_blank)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.diff_des_blank[index]['diff'], True))
			self.aligned_des_blank.append([refPressure, x1])

		self.aligned_average = []
		for index in range(len(self.aligned_des_blank[0][1])):
			value = [val[1][index] for val in self.aligned_des_blank]
			avg_value = sum(value)/len(self.aligned_des_blank)
			self.aligned_average.append(avg_value)
		
		self.average_diff_des_blank = [refPressure, self.aligned_average]
		

		# print "average_diff_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.average_diff_des_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_des_blank"

	

	def analyseAliq(self):
		##
		## self.average_DES_aliq, self.average_des_aliq, self.diff_DES_aliq, self.diff_des_aliq
		##
		#Total Average computations
		#Asbsorption align
		refPressure = None
		self.aligned_ads_aliq = []

		#Determine the reference
		if len(self.ads_aliq) > 0:
			refPressure = []
			for index in range(len(self.ads_aliq[0][0])):
				value = [val[0][index] for val in self.ads_aliq]
				avg_value = sum(value)/len(self.ads_aliq)
				refPressure.append(avg_value)

		#Align all the rest
		for index in range(len(self.ads_aliq)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.ads_aliq[index]))
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			self.aligned_ads_aliq.append([refPressure, x1])
		
		# self.aligned_average = []
		# for index in range(len(self.aligned_DES_aliq[0][1])):
		# 	value = [val[1][index] for val in self.aligned_DES_aliq]
		# 	avg_value = sum(value)/len(self.aligned_DES_aliq)
		# 	self.aligned_average.append(avg_value)
			
		# self.average_DES_aliq = [refPressure, self.aligned_average]

#######################################################################################
#######################################################################################

		#Desorbtion align
		refPressure= None
		self.aligned_des_aliq = []
		
		#Determine the reference
		if len(self.des_aliq) > 0:
			refPressure = []
			for index in range(len(self.des_aliq[0][0])):
				value = [val[0][index] for val in self.des_aliq]
				avg_value = sum(value)/len(self.des_aliq)
				refPressure.append(avg_value)

		#Align all the rest
		for index in range(len(self.des_aliq)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.des_aliq[index], True))
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			self.aligned_des_aliq.append([refPressure, x1])

		self.aligned_average = []
		
		##
		#Comabinatorial diff computations

		line = [0 for x in xrange(len(self.ads_aliq))]
		already = [line[:] for x in xrange(len(self.ads_aliq))]

		for indexI in range(0, len(self.ads_aliq)):
			for indexJ in range(0, len(self.ads_aliq)):

				if indexI == indexJ:
					# Do not compute same element case
					already[indexI][indexJ] = 0
					already[indexJ][indexI] = 0
				else:
					if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
					# Leave asymetric stuff for now. Later we could use it to average
					# for better approximation??? More dig is needed.
						already[indexJ][indexI] = 0
						already[indexI][indexJ] = 0
					else:
						# Computing self.ads_aliq[indexI] - self.ads_aliq[indexJ]
						# self.ads_aliq[indexJ] as to be self.aligned.

						interpolateK = self.align(self.ads_aliq[indexJ][0], self.ads_aliq[indexI])
						diffJK = self.diff(self.ads_aliq[indexJ][1], interpolateK)

						d = diffJK
						upperQR = np.percentile(d, 75, interpolation='higher')
						lowerQR = np.percentile(d, 25, interpolation='lower')
						innerQR = upperQR - lowerQR
						limit = upperQR + (12*innerQR)

						problem = False
						for el in diffJK:
							if el > limit:
								problem = True

						if not problem:
							self.diff_ads_aliq.append({'i':indexI, 'j':indexJ, 'diff':[self.ads_aliq[indexJ][0], diffJK]})
				

		# print "diff_DES_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_DES_aliq)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_DES_aliq"

		line = [0 for x in xrange(len(self.des_aliq))]
		already = [line[:] for x in xrange(len(self.des_aliq))]

		for indexI in range(0, len(self.des_aliq)):
			for indexJ in range(0, len(self.des_aliq)):

				if indexI == indexJ:
					# Do not compute same element case
					already[indexI][indexJ] = 0
					already[indexJ][indexI] = 0
				else:
					if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
					# Leave asymetric stuff for now. Later we could use it to average
					# for better approximation??? More dig is needed.
						already[indexJ][indexI] = 0
						already[indexI][indexJ] = 0
					else:
						# Computing self.DES_aliq[indexI] - self.DES_aliq[indexJ]
						# self.DES_aliq[indexJ] as to be self.aligned.
						# Computing self.DES_aliq[indexI] - self.DES_aliq[indexJ]
						# self.DES_aliq[indexJ] as to be self.aligned.
						interpolateK = self.align(self.des_aliq[indexJ][0], self.des_aliq[indexI], True)
						diffJK = self.diff(self.des_aliq[indexJ][1], interpolateK)

						d = diffJK
						upperQR = np.percentile(d, 75, interpolation='higher')
						lowerQR = np.percentile(d, 25, interpolation='lower')
						innerQR = upperQR - lowerQR
						limit = upperQR + (12*innerQR)

						problem = False
						for el in diffJK:
							if el > limit:
								problem = True

						if not problem:
							self.diff_des_aliq.append({'i':indexI, 'j':indexJ, 'diff':[self.des_aliq[indexJ][0], diffJK]})
						else:
							print "Problem %d %d"%(indexI, indexJ)
	
		##
		#Average diff computations
		#Asbsorption align
		refPressure = None
		self.aligned_diff_ads_aliq = []

		#Determine the reference
		if len(self.diff_ads_aliq) > 0:
			refPressure = []
			for index in range(len(self.diff_ads_aliq[0]['diff'][0])):
				value = [val['diff'][0][index] for val in self.diff_ads_aliq]
				avg_value = sum(value)/len(self.diff_ads_aliq)
				refPressure.append(avg_value)
		
		#Align all the rest
		for index in range(len(self.diff_ads_aliq)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.diff_ads_aliq[index]['diff']))
			self.aligned_diff_ads_aliq.append([refPressure, x1])

		self.average_diff_ads_aliq = []
		for index in range(len(self.aligned_diff_ads_aliq[0][1])):
			value = [val[1][index] for val in self.aligned_diff_ads_aliq]
			avg_value = sum(value)/len(self.aligned_diff_ads_aliq)
			self.average_diff_ads_aliq.append(avg_value)
	
		self.average_diff_ads_aliq = [refPressure, self.average_diff_ads_aliq]

#######################################################################################
#######################################################################################

		#Desorbtion align
		refPressure= None
		self.aligned_diff_des_aliq = []

		#Determine the reference
		if len(self.diff_des_aliq) > 0:
			refPressure = []
			for index in range(len(self.diff_des_aliq[0]['diff'][0])):
				value = [val['diff'][0][index] for val in self.diff_des_aliq]
				avg_value = sum(value)/len(self.diff_des_aliq)
				refPressure.append(avg_value)
			
		#Align all the rest
		for index in range(len(self.diff_des_aliq)):
			x1 = []
			
			x1.extend(self.align(refPressure, self.diff_des_aliq[index]['diff'], True))
			self.aligned_diff_des_aliq.append([refPressure, x1])

		self.average_diff_des_aliq = []
		for index in range(len(self.aligned_diff_des_aliq[0][1])):
			value = [val[1][index] for val in self.aligned_diff_des_aliq]
			avg_value = sum(value)/len(self.aligned_diff_des_aliq)
			self.average_diff_des_aliq.append(avg_value)
	
		self.average_diff_des_aliq = [refPressure, self.average_diff_des_aliq]
		

	def adsPlotsCombine(self):

		self.ADS_aliqRaw_list = []
		self.ADS_aliqBlank1_list = []
		self.ADS_aliqBlank2_list = []
		self.ADS_aliqBlank_many_list = []
		self.ADS_blankDiff_list = []
		self.ADS_blank1_diff_list = []
		self.ADS_blank2_diff_list = []
		self.ADSblank1_compareAll_list = []
		self.ADSblank2_compareAll_list = []
		self.ADSaliqBlank_compareAll_list = []

		ADSaliq_average = []
		ADSblank1_average = []
		ADSblank2_average = []

		diff_aliqBlank1_list = []
		diff_aliqBlank2_list = []
		blankDiff_list = []

		diff_aliqRaw_aliqBlank1_list = []
		diff_aliqRaw_aliqBlank2_list = []
		diff_aliqBlank1_aliqBlank2_list = []

		for index in range(len(self.ADSdelta_mass_aliq2_listMain[0])):
			
			aliq_value = [val[index] for val in self.ADSdelta_mass_aliq2_listMain]
			blank1_value = [val[index] for val in self.ADS_Aliq1_blankMain]
			blank2_value = [val[index] for val in self.ADS_Aliq2_blankMain]

			aliq_avg_value = sum(aliq_value)/len(self.ADSdelta_mass_aliq2_listMain)
			blank1_avg_value = sum(blank1_value)/len(self.ADS_Aliq1_blankMain)
			blank2_avg_value = sum(blank2_value)/len(self.ADS_Aliq2_blankMain)
			
			ADSaliq_average.append(aliq_avg_value)
			ADSblank1_average.append(blank1_avg_value)
			ADSblank2_average.append(blank2_avg_value)

		self.ADS_aliqRaw_list.extend([self.ADSrefPressure, ADSaliq_average])

		for val in range(len(self.ADSdelta_mass_aliq2_listMain[0])):
			
			xVal = ADSaliq_average[val]
			b1Val = ADSblank1_average[val]
			b2Val = ADSblank2_average[val]

			diff_aliqB1 = (xVal - b1Val)
			diff_aliqB2 = (xVal - b2Val)

		####################################################################################################################

			diff_aliqRaw_aliqBlank1 = xVal - diff_aliqB1
			diff_aliqRaw_aliqBlank1_list.append(diff_aliqRaw_aliqBlank1)

			diff_aliqRaw_aliqBlank2 = xVal - diff_aliqB2
			diff_aliqRaw_aliqBlank2_list.append(diff_aliqRaw_aliqBlank2)

			diff_aliqBlank1_aliqBlank2 = diff_aliqB1 - diff_aliqB2
			diff_aliqBlank1_aliqBlank2_list.append(diff_aliqBlank1_aliqBlank2)

		####################################################################################################################

			blankDiff = abs(b1Val - b2Val)

			diff_aliqBlank1_list.append(diff_aliqB1)
			diff_aliqBlank2_list.append(diff_aliqB2)

			blankDiff_list.append(blankDiff)

############################################################################################################################

		self.ADS_aliqBlank1_list.extend([self.ADSrefPressure, diff_aliqBlank1_list])
		self.ADS_aliqBlank2_list.extend([self.ADSrefPressure, diff_aliqBlank2_list])

		self.ADS_blank1_diff_list.extend([self.ADSrefPressure, ADSblank1_average])
		self.ADS_blank2_diff_list.extend([self.ADSrefPressure, ADSblank2_average])
		self.ADS_blankDiff_list.extend([self.ADSrefPressure, blankDiff_list])
		
		self.ADS_aliqBlank_many_list.extend([self.ADS_aliqRaw_list, self.ADS_aliqBlank1_list, self.ADS_aliqBlank2_list])

############################################################################################################################

		self.blank1_list1 = [self.ADSrefPressure, self.ADS_Aliq1_blankMain[0]]
		self.blank1_list2 = [self.ADSrefPressure, self.ADS_Aliq1_blankMain[1]]
		self.blank1_list3 = [self.ADSrefPressure, self.ADS_Aliq1_blankMain[2]]
		self.blank1_listAvg = [self.ADSrefPressure, ADSblank1_average]

		self.ADSblank1_compareAll_list.extend([self.blank1_list1, self.blank1_list2, self.blank1_list3, self.blank1_listAvg])

		self.blank2_list1 = [self.ADSrefPressure, self.ADS_Aliq2_blankMain[0]]
		self.blank2_list2 = [self.ADSrefPressure, self.ADS_Aliq2_blankMain[1]]
		self.blank2_list3 = [self.ADSrefPressure, self.ADS_Aliq2_blankMain[2]]
		self.blank2_listAvg = [self.ADSrefPressure, ADSblank2_average]

		self.ADSblank2_compareAll_list.extend([self.blank2_list1, self.blank2_list2, self.blank2_list3, self.blank2_listAvg])

############################################################################################################################
		
		self.ADSaliqBlank_compareAll_list.extend([[self.ADSrefPressure, diff_aliqRaw_aliqBlank1_list],\
												  [self.ADSrefPressure, diff_aliqRaw_aliqBlank2_list],\
												  [self.ADSrefPressure, diff_aliqBlank1_aliqBlank2_list]])


	def desPlotsCombine(self):

		self.DES_aliqRaw_list = []
		self.DES_aliqBlank1_list = []
		self.DES_aliqBlank2_list = []
		self.DES_aliqBlank_many_list = []
		self.DES_blankDiff_list = []
		self.DES_blank1_diff_list = []
		self.DES_blank2_diff_list = []
		self.DESblank1_compareAll_list = []
		self.DESblank2_compareAll_list = []
		self.DESaliqBlank_compareAll_list = []

		DESaliq_average = []
		DESblank1_average = []
		DESblank2_average = []

		diff_aliqBlank1_list = []
		diff_aliqBlank2_list = []
		blankDiff_list = []

		diff_aliqRaw_aliqBlank1_list = []
		diff_aliqRaw_aliqBlank2_list = []
		diff_aliqBlank1_aliqBlank2_list = []

		for index in range(len(self.DESdelta_mass_aliq2_listMain[0])):
			
			aliq_value = [val[index] for val in self.DESdelta_mass_aliq2_listMain]
			blank1_value = [val[index] for val in self.DES_Aliq1_blankMain]
			blank2_value = [val[index] for val in self.DES_Aliq2_blankMain]

			aliq_avg_value = sum(aliq_value)/len(self.DESdelta_mass_aliq2_listMain)
			blank1_avg_value = sum(blank1_value)/len(self.DES_Aliq1_blankMain)
			blank2_avg_value = sum(blank2_value)/len(self.DES_Aliq2_blankMain)
			
			DESaliq_average.append(aliq_avg_value)
			DESblank1_average.append(blank1_avg_value)
			DESblank2_average.append(blank2_avg_value)

		self.DES_aliqRaw_list.extend([self.DESrefPressure, DESaliq_average])

		for val in range(len(self.DESdelta_mass_aliq2_listMain[0])):

			xVal = DESaliq_average[val]
			b1Val = DESblank1_average[val]
			b2Val = DESblank2_average[val]

			diff_aliqB1 = (xVal - b1Val)
			diff_aliqB2 = (xVal - b2Val)

		####################################################################################################################

			diff_aliqRaw_aliqBlank1 = xVal - diff_aliqB1
			diff_aliqRaw_aliqBlank1_list.append(diff_aliqRaw_aliqBlank1)

			diff_aliqRaw_aliqBlank2 = xVal - diff_aliqB2
			diff_aliqRaw_aliqBlank2_list.append(diff_aliqRaw_aliqBlank2)

			diff_aliqBlank1_aliqBlank2 = diff_aliqB1 - diff_aliqB2
			diff_aliqBlank1_aliqBlank2_list.append(diff_aliqBlank1_aliqBlank2)

		####################################################################################################################

			blankDiff = abs(b1Val - b2Val)

			diff_aliqBlank1_list.append(diff_aliqB1)
			diff_aliqBlank2_list.append(diff_aliqB2)

			blankDiff_list.append(blankDiff)

# ############################################################################################################################

# 		self.DES_aliqBlank1_list.extend([self.DESrefPressure, diff_aliqBlank1_list])
# 		self.DES_aliqBlank2_list.extend([self.DESrefPressure, diff_aliqBlank2_list])

# 		self.DES_aliqBlank_many_list.extend([self.DES_aliqRaw_list, self.DES_aliqBlank1_list, self.DES_aliqBlank2_list])

# 		self.DES_blankDiff_list.extend([self.DESrefPressure, blankDiff_list])

# ############################################################################################################################

# 		self.blank1_list1 = [self.DESrefPressure, self.DES_Aliq1_blankMain[0]]
# 		self.blank1_list2 = [self.DESrefPressure, self.DES_Aliq1_blankMain[1]]
# 		self.blank1_list3 = [self.DESrefPressure, self.DES_Aliq1_blankMain[2]]
# 		self.blank1_listAvg = [self.DESrefPressure, DESblank1_average]

# 		self.DESblank1_compareAll_list.extend([self.blank1_list1, self.blank1_list2, self.blank1_list3, self.blank1_listAvg])

# 		self.blank2_list1 = [self.DESrefPressure, self.DES_Aliq2_blankMain[0]]
# 		self.blank2_list2 = [self.DESrefPressure, self.DES_Aliq2_blankMain[1]]
# 		self.blank2_list3 = [self.DESrefPressure, self.DES_Aliq2_blankMain[2]]
# 		self.blank2_listAvg = [self.DESrefPressure, DESblank2_average]

# 		self.DESblank2_compareAll_list.extend([self.blank2_list1, self.blank2_list2, self.blank2_list3, self.blank2_listAvg])

# ############################################################################################################################

# 		self.DESaliqBlank_compareAll_list.extend([[self.DESrefPressure, diff_aliqRaw_aliqBlank1_list],\
# 												  [self.DESrefPressure, diff_aliqRaw_aliqBlank2_list],\
# 												  [self.DESrefPressure, diff_aliqBlank1_aliqBlank2_list]])

############################################################################################################################

		self.DES_aliqBlank1_list.extend([self.DESrefPressure, diff_aliqBlank1_list])
		self.DES_aliqBlank2_list.extend([self.DESrefPressure, diff_aliqBlank2_list])

		self.DES_blank1_diff_list.extend([self.DESrefPressure, DESblank1_average])
		self.DES_blank2_diff_list.extend([self.DESrefPressure, DESblank2_average])
		self.DES_blankDiff_list.extend([self.DESrefPressure, blankDiff_list])
		
		self.DES_aliqBlank_many_list.extend([self.DES_aliqRaw_list, self.DES_aliqBlank1_list, self.DES_aliqBlank2_list])

############################################################################################################################

		self.blank1_list1 = [self.DESrefPressure, self.DES_Aliq1_blankMain[0]]
		self.blank1_list2 = [self.DESrefPressure, self.DES_Aliq1_blankMain[1]]
		self.blank1_list3 = [self.DESrefPressure, self.DES_Aliq1_blankMain[2]]
		self.blank1_listAvg = [self.DESrefPressure, DESblank1_average]

		self.DESblank1_compareAll_list.extend([self.blank1_list1, self.blank1_list2, self.blank1_list3, self.blank1_listAvg])

		self.blank2_list1 = [self.DESrefPressure, self.DES_Aliq2_blankMain[0]]
		self.blank2_list2 = [self.DESrefPressure, self.DES_Aliq2_blankMain[1]]
		self.blank2_list3 = [self.DESrefPressure, self.DES_Aliq2_blankMain[2]]
		self.blank2_listAvg = [self.DESrefPressure, DESblank2_average]

		self.DESblank2_compareAll_list.extend([self.blank2_list1, self.blank2_list2, self.blank2_list3, self.blank2_listAvg])

############################################################################################################################
		
		self.DESaliqBlank_compareAll_list.extend([[self.DESrefPressure, diff_aliqRaw_aliqBlank1_list],\
												  [self.DESrefPressure, diff_aliqRaw_aliqBlank2_list],\
												  [self.DESrefPressure, diff_aliqBlank1_aliqBlank2_list]])

	def mainPlotsAliq(self):
			
		aliqNum = 0
		self.ADSdelta_mass_aliq2_listMain = []
		self.DESdelta_mass_aliq2_listMain = []
		for file in glob.glob("TGA/Data_Files/JSON/json_aliq/*.json"):
			aliqPart = file.split("/")[-1]
			find_aliq = re.search('Aliq2', aliqPart)

			if find_aliq:
			
				content = None
				print aliqNum
				with open(file, "r") as aliq_file:
					content = aliq_file.read()
					raw = json.loads(content)
					blocks = self.split(raw, run = 2)
					# print blocks
					conc_listAds = []
					conc_listDes = []

					for i in range(len(self.ads_aliq[0][0])):
						conc_listAds.append(blocks[0][1][0])
					for j in range(len(self.des_aliq[0][0])):
						conc_listDes.append(blocks[0][1][0])
					# print conc_listDES
					# print conc_listDes
					self.ADS_aliqMain.extend([blocks[0][0], conc_listAds])
					self.DES_aliqMain.extend([blocks[1][0], conc_listDes])

############################ DESorption/Desorption: Aliq2 ###############################
					
					self.ADSrefPressure = self.aligned_ads_aliq[0][0]
					self.DESrefPressure = self.aligned_des_aliq[0][0]		

					ADSaligned_aliq2_weight2_vals = []
					ADSaligned_aliq2_norm_list = []
					ADSdelta_mass_aliq2_list = []
					# self.ADSdelta_mass_aliq2_listMain = []

					ADSaligned_aliq2_weight2_vals.extend(self.align(self.ADSrefPressure, self.ADS_aliqMain))
					print self.aligned_ads_aliq
					# print ADSaligned_aliq2_norm_list
					ADSaligned_aliq2_norm_list.extend(self.aligned_ads_aliq[aliqNum])
					
					
					for x in range(len(ADSaligned_aliq2_norm_list[0])):
						i = ADSaligned_aliq2_weight2_vals[x]
						j = ADSaligned_aliq2_norm_list[1][x]

						ADSdelta_mass_val = (i*j)/100
						ADSdelta_mass_aliq2_list.append(ADSdelta_mass_val)
					self.ADSdelta_mass_aliq2_listMain.append(ADSdelta_mass_aliq2_list)

					DESaligned_aliq2_weight2_vals = []
					DESaligned_aliq2_norm_list = []
					DESdelta_mass_aliq2_list = []
					# self.DESdelta_mass_aliq2_listMain = []

					DESaligned_aliq2_weight2_vals.extend(self.align(self.DESrefPressure, self.DES_aliqMain))										
					DESaligned_aliq2_norm_list.extend(self.aligned_des_aliq[aliqNum])
				
					for y in range(len(DESaligned_aliq2_norm_list[0])):
						i = DESaligned_aliq2_weight2_vals[y]
						j = DESaligned_aliq2_norm_list[1][y]
						
						DESdelta_mass_val = (i*j)/100
						DESdelta_mass_aliq2_list.append(DESdelta_mass_val)
					self.DESdelta_mass_aliq2_listMain.append(DESdelta_mass_aliq2_list)

				aliqNum += 1
		
		
	def mainPlotsBlank(self):
		
		blankNum1 = 0
		blankNum2 = 0

		self.ADS_Aliq1_blankMain = []
		self.DES_Aliq1_blankMain = []
		self.ADS_Aliq2_blankMain = []
		self.DES_Aliq2_blankMain = []
		for file in glob.glob("TGA/Data_Files/JSON/json_blank/*.json"):
			blankPart = file.split("/")[-1]
			find_blankAliq1 = re.search('Aliq1', blankPart)
			find_blankAliq2 = re.search('Aliq2', blankPart)
			if find_blankAliq1:

				conc_listBlankAds = []
				conc_listBlankDes = []
				ADS_blankMain = []
				DES_blankMain = []

				content = None
				with open(file, "r") as blank_file:
					print "Blank Num1: %s"%blankNum1
					content = blank_file.read()
					raw = json.loads(content)
					blocks = self.split(raw, run = 2)

					for i in range(len(self.ads_aliq[0][0])):
						conc_listBlankAds.append(blocks[0][1][0])
					for j in range(len(self.des_aliq[0][0])):
						conc_listBlankDes.append(blocks[0][1][0])

					ADS_blankMain.extend([blocks[0][0], conc_listBlankAds])
					DES_blankMain.extend([blocks[1][0], conc_listBlankDes])
					
# ############################ DESorption: blank ###############################		

					ADSaligned_blank_weight2_vals = []
					ADSaligned_blank_norm_list = []
					ADSdelta_mass_blank_list = []
						
					ADSaligned_blank_weight2_vals.extend(self.align(self.ADSrefPressure, ADS_blankMain))
					ADSaligned_blank_norm_list.extend(self.aligned_ads_blank[blankNum1])
				
					for x in range(len(ADSaligned_blank_norm_list[0])):
						i = ADSaligned_blank_weight2_vals[x]
						j = ADSaligned_blank_norm_list[1][x]
						
						ADSdelta_mass_val = (i*j)/100
						ADSdelta_mass_blank_list.append(ADSdelta_mass_val)	
					self.ADS_Aliq1_blankMain.append(ADSdelta_mass_blank_list)

		############################ Desorption: blank ###############################

					DESaligned_blank_weight2_vals = []
					DESaligned_blank_norm_list = []
					DESdelta_mass_blank_list = []
					
					DESaligned_blank_weight2_vals.extend(self.align(self.DESrefPressure, DES_blankMain))										
					DESaligned_blank_norm_list.extend(self.aligned_des_blank[blankNum1])
					
					for y in range(len(DESaligned_blank_norm_list[0])):
						
						i = DESaligned_blank_weight2_vals[y]
						j = DESaligned_blank_norm_list[1][y]
						
						DESdelta_mass_val = (i*j)/100
						DESdelta_mass_blank_list.append(DESdelta_mass_val)
					self.DES_Aliq1_blankMain.append(DESdelta_mass_blank_list)

				blankNum1 += 1		

			if find_blankAliq2:
				
				conc_listBlankAds = []
				conc_listBlankDes = []
				ADS_blankMain = []
				DES_blankMain = []
				
				content = None
				with open(file, "r") as blank_file:
					print "Blank Num2: %s"%blankNum2
					content = blank_file.read()
					raw = json.loads(content)
					blocks = self.split(raw, run = 2)

					for i in range(len(self.ads_aliq[0][0])):
						conc_listBlankAds.append(blocks[0][1][0])
					for j in range(len(self.des_aliq[0][0])):
						conc_listBlankDes.append(blocks[0][1][0])

					ADS_blankMain.extend([blocks[0][0], conc_listBlankAds])
					DES_blankMain.extend([blocks[1][0], conc_listBlankDes])
					
# ############################ DESorption: blank ###############################		

					ADSaligned_blank_weight2_vals = []
					ADSaligned_blank_norm_list = []
					ADSdelta_mass_blank_list = []
						
					ADSaligned_blank_weight2_vals.extend(self.align(self.ADSrefPressure, ADS_blankMain))
					ADSaligned_blank_norm_list.extend(self.aligned_ads_blank[blankNum2])
				
					for x in range(len(ADSaligned_blank_norm_list[0])):
						
						i = ADSaligned_blank_weight2_vals[x]
						j = ADSaligned_blank_norm_list[1][x]
						
						ADSdelta_mass_val = (i*j)/100
						ADSdelta_mass_blank_list.append(ADSdelta_mass_val)		
					self.ADS_Aliq2_blankMain.append(ADSdelta_mass_blank_list)
		############################ Desorption: blank ###############################

					DESaligned_blank_weight2_vals = []
					DESaligned_blank_norm_list = []
					DESdelta_mass_blank_list = []
					
					DESaligned_blank_weight2_vals.extend(self.align(self.DESrefPressure, DES_blankMain))										
					DESaligned_blank_norm_list.extend(self.aligned_des_blank[blankNum1])
					
					for y in range(len(DESaligned_blank_norm_list[0])):
						
						i = DESaligned_blank_weight2_vals[y]
						j = DESaligned_blank_norm_list[1][y]
						
						DESdelta_mass_val = (i*j)/100
						DESdelta_mass_blank_list.append(DESdelta_mass_val)
					self.DES_Aliq2_blankMain.append(DESdelta_mass_blank_list)

				blankNum2 += 1		

	def analyseAll(self):
		self.analyseAliq()
		self.analyseBlank()
		self.mainPlotsAliq()
		self.mainPlotsBlank()
		self.adsPlotsCombine()
		self.desPlotsCombine()
		

		


		


		








