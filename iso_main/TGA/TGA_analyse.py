# import numpy as np
# import glob, os
# import simplejson as json 

# class TGA_Analyse:
# 	def __init__(self):

# 		self.origin_blanks = []
# 		self.origin_aliqs = []

# 		# blanks data
# 		self.ads_blank = []
# 		self.des_blank = []

# 		# aliqs data
# 		self.ads_aliq = []
# 		self.des_aliq = []

# 		# diff blanks data
# 		self.diff_ads_blank = []
# 		self.diff_des_blank = []

# 		# diff aliqs data
# 		self.diff_ads_aliq = []
# 		self.diff_des_aliq = []

# 		# average blanks data
# 		self.average_ads_blank = []
# 		self.average_des_blank = []

# 		# average aliqs data
# 		self.average_ads_aliq = []
# 		self.average_des_aliq = []

# 		# average diffs blanks data
# 		self.average_diff_ads_blank = []
# 		self.average_diff_des_blank = []

# 		# average diffs aliqs data
# 		self.average_diff_ads_aliq = []
# 		self.average_diff_des_aliq = []

# 		# corrected aliqs
# 		self.corrected_ads_aliq = []
# 		self.corrected_des_aliq = []

# 		# corrected average aliqs data
# 		self.average_corrected_ads_aliq = []
# 		self.average_corrected_des_aliq = []

# 	def load(self):
# 		# blanks = []
# 		# alisqs = []
# 		os.chdir(os.path.dirname(os.getcwd()))
# 		index = 0
# 		for file in glob.glob("TGA/Data_Files/JSON/json_aliq/*.json"):
			
# 			content = None
# 			with open(file, "r") as aliq_file:
# 				content = aliq_file.read()

# 			raw = json.loads(content)
# 			# alisqs.append(raw)
# 			blocks = self.split(raw)
# 			self.ads_aliq.append(blocks[0])
# 			self.des_aliq.append(blocks[1])
# 			filePart = file.split("/")[-1].split("_")[:4]
			
# 			aliqLabel = '_'.join(filePart)
# 			self.origin_aliqs.append(aliqLabel)

# 			index += 1

# 		# os.chdir(os.path.dirname(os.getcwd()))
# 		index = 0
# 		for file in glob.glob("TGA/Data_Files/JSON/json_blankRuns/*.json"):
# 			content = None
# 			with open(file, "r") as blank_file:
# 				content = blank_file.read()

# 			raw = json.loads(content)
# 			# blanks.append(raw)
# 			blocks = self.split(raw)
# 			self.ads_blank.append(blocks[0])
# 			self.des_blank.append(blocks[1])
# 			filePart = file.split("/")[-1].split("_")[:4]
			
# 			blankLabel = '_'.join(filePart)
# 			self.origin_blanks.append(blankLabel)
			
# 			index += 1

# 	def split(self, raw):

# 		begin3 = 1

# 		pressure_list = []
# 		conc_list = []

# 		while True: 
# 			try:
# 				content= raw["content"][begin3 - 1]

# 				conc_dict = content.get('weights')[4] # Before it was 3 but corrected to 4th.
# 				conc_val = conc_dict.get('value')

# 				pressure_dict = content.get('pressure')
# 				pressure_val = pressure_dict.get('value')

# 				pressure_list.append(pressure_val)
# 				conc_list.append(conc_val)
					
# 				begin3 +=1

# 			except:
# 				break

# 		total = len(pressure_list)

# 		pressure_listA1 = []
# 		conc_list1 = []

# 		pressure_list2 = []
# 		conc_listA2 = []
		
# 		boundary = -1
# 		for t in range(total):
# 			if t == total - 1:
# 				break
# 			elif t > 0:
# 				if pressure_list[t] >= pressure_list[t + 1] and pressure_list[t] >= pressure_list[t - 1]:
# 					boundary = t
# 					break
# 				if pressure_list[t] <= pressure_list[t + 1] and pressure_list[t] <= pressure_list[t - 1]:
# 					boundary = t
# 					break

# 		pressure_listA1 = list(pressure_list[0:boundary])
# 		pressure_list2 = list(pressure_list[boundary + 1:len(pressure_list) - 1])

# 		conc_list1 = list(conc_list[0:boundary])
# 		conc_listA2 = list(conc_list[boundary + 1:len(conc_list) - 1])

# 		return [[pressure_listA1, conc_list1], [pressure_list2, conc_listA2]]

# 	# x array to interpolate
# 	# The sampling.
# 	def align(self, dataX, dataXY, reverse=False):
# 		# print "dataX+++++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(dataX)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++++dataX"

# 		# print "dataXY+++++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(dataXY)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++++dataXY"

# 		UNDEF = -99.0

# 		if reverse:
# 			aligned = list(reversed(np.interp(list(reversed(dataX)), list(reversed(dataXY[0])), list(reversed(dataXY[1])), right=UNDEF)))
# 		else:
# 			aligned = list(np.interp(dataX, dataXY[0], dataXY[1], right=UNDEF))

# 		# print "aligned++++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(aligned)
# 		# print "++++++++++++++++++++++++++++++++++++++++++++++++aligned"

# 		return aligned

# 	def diff(self, dataY1, dataY2):
# 		dataSub = np.array(dataY1) - np.array(dataY2)
# 		return [abs(data) for data in list(dataSub)]

# 	def average(self, dataY):
# 		# print "dataY+++++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(dataY)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++++dataY"
# 		averageY = [0.00 for d in dataY[0]]
# 		for data in dataY:
# 			for index in range(len(data)):
# 				averageY[index] += data[index]

# 		average = [float(d/len(averageY)) for d in averageY]

# 		print "average+++++++++++++++++++++++++++++++++++++++++++++++"
# 		print json.dumps(len(averageY))
# 		print json.dumps(averageY)
# 		print json.dumps(average)
# 		print "+++++++++++++++++++++++++++++++++++++++++++++++average"

# 		return average

# 	def analyseBlank(self):
# 		##
# 		## self.average_ads_blank, self.average_des_blank, self.diff_ads_blank, self.diff_des_blank
# 		##
# 		#Total Average computations
# 		#Asbsorption align
# 		refPressure= None
# 		aligned_ads_blank = []

# 		#Determine the reference
# 		if len(self.ads_blank) > 0:
# 			refPressure = self.ads_blank[0][0]

# 		#Align all the rest
# 		for index in range(1, len(self.ads_blank)):
# 			#(pressure, concentration): [0], [1]
# 			aligned_ads_blank.append([refPressure, self.align(refPressure, self.ads_blank[index])])

# 		self.average_ads_blank = [refPressure, self.average([data[1] for data in aligned_ads_blank])]

# 		#Desorbtion align
# 		refPressure= None
# 		aligned_des_blank = []

# 		#Determine the reference
# 		if len(self.des_blank) > 0:
# 			refPressure = self.des_blank[0][0]

# 		#Align all the rest
# 		for index in range(1, len(self.des_blank)):
# 			#(pressure, concentration): [0], [1]
# 			aligned_des_blank.append([refPressure, self.align(refPressure, self.des_blank[index], True)])

# 		self.average_des_blank = [refPressure, self.average([data[1] for data in aligned_des_blank])]

# 		##
# 		#Comabinatorial diff computations

# 		line = [0 for x in xrange(len(self.ads_blank))]
# 		already = [line[:] for x in xrange(len(self.ads_blank))]

# 		for indexI in range(0, len(self.ads_blank)):
# 			for indexJ in range(0, len(self.ads_blank)):
# 				if indexI == indexJ:
# 					# Do not compute same element case
# 					already[indexI][indexJ] = 1
# 				if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
# 					# Leave asymetric stuff for now. Later we could use it to average
# 					# for better approximation??? More dig is needed.
# 					already[indexI][indexJ] = 1
# 					already[indexJ][indexI] = 1
# 				else:
# 					# Computing self.ads_blank[indexI] - self.ads_blank[indexJ]
# 					# self.ads_blank[indexJ] as to be aligned.

# 					interpolateK = self.align(self.ads_blank[indexJ][0], self.ads_blank[indexI])
# 					diffJK = self.diff(self.ads_blank[indexJ][1], interpolateK)

# 					self.diff_ads_blank.append({'i':indexI, 'j':indexJ, 'diff':[self.ads_blank[indexJ][0], diffJK]})

# 		# print "diff_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.diff_ads_blank)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_ads_blank"

# 		line = [0 for x in xrange(len(self.des_blank))]
# 		already = [line[:] for x in xrange(len(self.des_blank))]

# 		for indexI in range(0, len(self.des_blank)):
# 			for indexJ in range(0, len(self.des_blank)):
# 				if indexI == indexJ:
# 					# Do not compute same element case
# 					already[indexI][indexJ] = 1
# 				if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
# 					# Leave asymetric stuff for now. Later we could use it to average
# 					# for better approximation??? More dig is needed.
# 					already[indexI][indexJ] = 1
# 					already[indexJ][indexI] = 1
# 				else:
# 					# Computing self.ads_blank[indexI] - self.ads_blank[indexJ]
# 					# self.ads_blank[indexJ] as to be aligned.

# 					interpolateK = self.align(self.des_blank[indexJ][0], self.des_blank[indexI], True)
# 					diffJK = self.diff(self.des_blank[indexJ][1], interpolateK)

# 					self.diff_des_blank.append({'i':indexI, 'j':indexJ, 'diff':[self.des_blank[indexJ][0], diffJK]})

# 		# print "diff_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.diff_des_blank)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_des_blank"

# 		##
# 		#Average diff computations
# 		#Asbsorption align
# 		refPressure= None
# 		aligned_ads_blank = []

# 		#Determine the reference
# 		if len(self.diff_ads_blank) > 0:
# 			refPressure = self.diff_ads_blank[0]['diff'][0]

# 		#Align all the rest
# 		for index in range(1, len(self.diff_ads_blank)):
# 			#(pressure, concentration): [0], [1]
# 			aligned_ads_blank.append([refPressure, self.align(refPressure, self.diff_ads_blank[index]['diff'])])

# 		self.average_diff_ads_blank = [refPressure, self.average([data[1] for data in aligned_ads_blank])]

# 		# print "average_diff_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.average_diff_ads_blank)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_ads_blank"

# 		#Desorbtion align
# 		refPressure= None
# 		aligned_des_blank = []

# 		#Determine the reference
# 		if len(self.des_blank) > 0:
# 			refPressure = self.diff_des_blank[0]['diff'][0]

# 		#Align all the rest
# 		for index in range(1, len(self.diff_des_blank)):
# 			#(pressure, concentration): [0], [1]
# 			aligned_des_blank.append([refPressure, self.align(refPressure, self.diff_des_blank[index]['diff'], True)])

# 		self.average_diff_des_blank = [refPressure, self.average([data[1] for data in aligned_des_blank])]

# 		# print "average_diff_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.average_diff_des_blank)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_des_blank"




# 	def analyseAliq(self):
# 		##
# 		## self.average_ads_aliq, self.average_des_aliq, self.diff_ads_aliq, self.diff_des_aliq
# 		##
# 		#Total Average computations
# 		#Asbsorption align
# 		refPressure= None
# 		aligned_ads_aliq = []

# 		#Determine the reference
# 		if len(self.ads_aliq) > 0:
# 			refPressure = self.ads_aliq[0][0]

# 		#Align all the rest
# 		for index in range(1, len(self.ads_aliq)):
# 			#(pressure, concentration): [0], [1]
# 			# print json.dumps(self.align(refPressure, self.ads_aliq[index]))
# 			aligned_ads_aliq.append([refPressure, self.align(refPressure, self.ads_aliq[index])])

# 		self.average_ads_aliq = [refPressure, self.average([data[1] for data in aligned_ads_aliq])]

# 		#Desorbtion align
# 		refPressure= None
# 		aligned_des_aliq = []

# 		#Determine the reference
# 		if len(self.des_aliq) > 0:
# 			refPressure = self.des_aliq[0][0]

# 		#Align all the rest
# 		for index in range(1, len(self.des_aliq)):
# 			#(pressure, concentration): [0], [1]
# 			aligned_des_aliq.append([refPressure, self.align(refPressure, self.des_aliq[index], True)])

# 		self.average_des_aliq = [refPressure, self.average([data[1] for data in aligned_des_aliq])]

# 		##
# 		#Comabinatorial diff computations

# 		line = [0 for x in xrange(len(self.ads_aliq))]
# 		already = [line[:] for x in xrange(len(self.ads_aliq))]

# 		for indexI in range(0, len(self.ads_aliq)):
# 			for indexJ in range(0, len(self.ads_aliq)):
# 				if indexI == indexJ:
# 					# Do not compute same element case
# 					already[indexI][indexJ] = 1
# 				if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
# 					# Leave asymetric stuff for now. Later we could use it to average
# 					# for better approximation??? More dig is needed.
# 					already[indexI][indexJ] = 1
# 					already[indexJ][indexI] = 1
# 				else:
# 					# Computing self.ads_aliq[indexI] - self.ads_aliq[indexJ]
# 					# self.ads_aliq[indexJ] as to be aligned.

# 					interpolateK = self.align(self.ads_aliq[indexJ][0], self.ads_aliq[indexI])
# 					diffJK = self.diff(self.ads_aliq[indexJ][1], interpolateK)

# 					self.diff_ads_aliq.append({'i':indexI, 'j':indexJ, 'diff':[self.ads_aliq[indexJ][0], diffJK]})

# 		# print "diff_ads_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.diff_ads_aliq)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_ads_aliq"

# 		line = [0 for x in xrange(len(self.des_aliq))]
# 		already = [line[:] for x in xrange(len(self.des_aliq))]

# 		for indexI in range(0, len(self.des_aliq)):
# 			for indexJ in range(0, len(self.des_aliq)):
# 				if indexI == indexJ:
# 					# Do not compute same element case
# 					already[indexI][indexJ] = 1
# 				if already[indexI][indexJ] == 1 or already[indexJ][indexI] == 1:
# 					# Leave asymetric stuff for now. Later we could use it to average
# 					# for better approximation??? More dig is needed.
# 					already[indexI][indexJ] = 1
# 					already[indexJ][indexI] = 1
# 				else:
# 					# Computing self.ads_aliq[indexI] - self.ads_aliq[indexJ]
# 					# self.ads_aliq[indexJ] as to be aligned.

# 					interpolateK = self.align(self.des_aliq[indexJ][0], self.des_aliq[indexI], True)
# 					diffJK = self.diff(self.des_aliq[indexJ][1], interpolateK)

# 					self.diff_des_aliq.append({'i':indexI, 'j':indexJ, 'diff':[self.des_aliq[indexJ][0], diffJK]})

# 		# print "diff_des_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.diff_des_aliq)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_des_aliq"

# 		##
# 		#Average diff computations
# 		#Asbsorption align
# 		refPressure= None
# 		aligned_ads_aliq = []

# 		#Determine the reference
# 		if len(self.diff_ads_aliq) > 0:
# 			refPressure = self.diff_ads_aliq[0]['diff'][0]

# 		#Align all the rest
# 		for index in range(1, len(self.diff_ads_aliq)):
# 			#(pressure, concentration): [0], [1]
# 			aligned_ads_aliq.append([refPressure, self.align(refPressure, self.diff_ads_aliq[index]['diff'])])

# 		self.average_diff_ads_aliq = [refPressure, self.average([data[1] for data in aligned_ads_aliq])]

# 		#Desorbtion align
# 		refPressure= None
# 		aligned_des_aliq = []

# 		#Determine the reference
# 		if len(self.des_aliq) > 0:
# 			refPressure = self.diff_des_aliq[0]['diff'][0]

# 		#Align all the rest
# 		for index in range(1, len(self.diff_des_aliq)):
# 			#(pressure, concentration): [0], [1]
# 			aligned_des_aliq.append([refPressure, self.align(refPressure, self.diff_des_aliq[index]['diff'], True)])

# 		self.average_diff_des_aliq = [refPressure, self.average([data[1] for data in aligned_des_aliq])]


# 	def analyseAll(self):
# 		self.analyseAliq()
# 		self.analyseBlank()

# 		# Plot average blank ads and des
# 		# print "average_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.average_ads_blank)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_ads_blank"

# 		# print "average_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.average_des_blank)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_des_blank"

# 		# Plot average diff ads and des

# 		# print "average_diff_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.average_diff_ads_blank)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_ads_blank"

# 		# print "average_diff_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.average_diff_des_blank)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_des_blank"

# 		# Plot blanks combinations and diff

# 		# print "blanks_and_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps([ {'blank1':self.ads_blank[diff['i']], 'blank2':self.ads_blank[diff['j']], 'diff':diff['diff']} for diff in self.diff_ads_blank])
# 		# print json.dumps([ {'blank1':self.des_blank[diff['i']], 'blank2':self.des_blank[diff['j']], 'diff':diff['diff']} for diff in self.diff_des_blank])
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++blanks_and_diffs"

# 		# Plot all the blanks diffs
# 		# print "blanks_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps([ diff['diff'] for diff in self.diff_ads_blank])
# 		# print json.dumps([ diff['diff'] for diff in self.diff_des_blank])
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++blanks_diffs"

# 		# Assessment1: Are the diffs zero?
# 		# Assessment2: if not zero, Are the diffs constant?
# 		# Assessment3: if not constant, Are the diff evolving? How? Can we quantify it?

# 		# Plot all the aliq diffs.
# 		# The machine error should be behind the variations of the diffs.
# 		# print "aliqs_and_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps([ {'aliq1':self.ads_aliq[diff['i']], 'aliq2':self.ads_aliq[diff['j']], 'diff':diff['diff']} for diff in self.diff_ads_aliq])
# 		# print json.dumps([ {'aliq1':self.des_aliq[diff['i']], 'aliq2':self.des_aliq[diff['j']], 'diff':diff['diff']} for diff in self.diff_des_aliq])
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++aliqs_and_diffs"
# 		# All the diff together compared to the average blanks
# 		# print "aliqs_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps([ diff['diff'] for diff in self.diff_ads_aliq])
# 		# print json.dumps(self.average_ads_blank)
# 		##
# 		# print json.dumps([ diff['diff'] for diff in self.diff_des_aliq])
# 		# print json.dumps(self.average_des_blank)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++aliqs_diffs"

# 		# Assessement4: Are the diffs of the aliq evolving the same way as the average of the blanks?
# 		# Correlation with the the previous 3 assessments. If the variation is constant then, the
# 		# evolution should be uniform and always the same for all aliq. The differences will not show anything.
# 		# Yet if the evolution is not uniform and the blanks diff is not constant then should all follow the same scheme.

# 		# +1: If blanks diff is constant: We can remove the blanks average from the aliq
# 		# and compare the aliq and correlated that they are closer to be the same then we can conclude 
# 		# by sharing the average blanks. And we can share a database of blanks that will always give back the average to all
# 		# scientists. The more blanks we have the more closer to the approximated blanks we have.

# 		# +2: If blanks diff is not constant: We should see that the aliqs diff and the blanks average evolve the same
# 		# way. Then we should quantify the blanks by approximating it and sharing it to all scientist also. Except this
# 		# case it is not a simple average but an approximation base on many variations.
# 		# Here we should also take out the approximated global blank from the aliq and confirm that all diffs tend be very close
# 		# to zeros.

# 		# We use here the average to correct the data because being constant or not or needing approximation,
# 		# substracted with the aliqs should eliminates differences residus.

# 		# Compute the corrected
# 		for aliq in self.ads_aliq:
# 			aligned_average_ads_blank = self.align(aliq[0], self.average_ads_blank)
# 			corrected_aliq = [aliq[0], self.diff(aliq[1], aligned_average_ads_blank)]
# 			self.corrected_ads_aliq.append(corrected_aliq)

# 		for aliq in self.des_aliq:
# 			aligned_average_des_blank = self.align(aliq[0], self.average_des_blank, True)
# 			corrected_aliq = [aliq[0], self.diff(aliq[1], aligned_average_des_blank)]
# 			self.corrected_des_aliq.append(corrected_aliq)

# 		# Computing the average corrected
# 		refPressure= None
# 		aligned_corrected_ads_aliq = []

# 		if len(self.corrected_ads_aliq) > 0:
# 			refPressure = self.corrected_ads_aliq[0][0]

# 		for index in range(1, len(self.corrected_ads_aliq)):
# 			aligned_corrected_ads_aliq.append([refPressure, self.align(refPressure, self.corrected_ads_aliq[index])])

# 		self.average_corrected_ads_aliq = [refPressure, self.average([data[1] for data in aligned_corrected_ads_aliq])]

# 		refPressure= None
# 		aligned_corrected_des_aliq = []

# 		if len(self.corrected_des_aliq) > 0:
# 			refPressure = self.corrected_des_aliq[0][0]

# 		for index in range(1, len(self.corrected_des_aliq)):
# 			aligned_corrected_des_aliq.append([refPressure, self.align(refPressure, self.corrected_des_aliq[index], True)])

# 		self.average_corrected_des_aliq = [refPressure, self.average([data[1] for data in aligned_corrected_des_aliq])]

# 		# print "corrected_ads_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.corrected_ads_aliq)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++corrected_ads_aliq"

# 		# print "corrected_des_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.corrected_des_aliq)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++corrected_des_aliq"

# 		# print "average_corrected_ads_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.average_corrected_ads_aliq)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_corrected_ads_aliq"

# 		# print "average_corrected_des_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
# 		# print json.dumps(self.average_corrected_des_aliq)
# 		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_corrected_des_aliq"

# 		# Finish analyse



############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

import numpy as np
import glob, os
import simplejson as json 

class TGA_Analyse:
	def __init__(self):

		self.diff_ads_blankMain = []
		self.diff_des_blankMain = []

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
		self.diff_ads_blank2 = []
		self.diff_des_blank2 = []

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
		for file in glob.glob("TGA/Data_Files/JSON/json_blankRuns/*.json"):
			content = None
			with open(file, "r") as blank_file:
				content = blank_file.read()

				raw = json.loads(content)
				# blanks.append(raw)
				blocks = self.split(raw, run = 1)
<<<<<<< HEAD

=======
				
>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008
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

<<<<<<< HEAD
				if run == 0: 
					conc_dict = content.get('weights')[3] # Before it was 3 but corrected to 4th and now second	
				elif run == 1:
					conc_dict = content.get('weights')[4]
=======
				if run == 0:
					conc_dict = content.get('weights')[1] # Before it was 3 but corrected to 4th and now second	
				elif run == 1: 
					conc_dict = content.get('weights')[4]

>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008
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
<<<<<<< HEAD
		
=======

>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008
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

<<<<<<< HEAD
		
=======

>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008
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
			aligned = list(reversed(np.interp(list(reversed(dataX)), list(reversed(dataXY[0])), list(reversed(dataXY[1])))))
			
		else:
			aligned = list(np.interp(dataX, dataXY[0], dataXY[1]))
		
		# print "aligned++++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(aligned)
		# print "++++++++++++++++++++++++++++++++++++++++++++++++aligned"

		return aligned

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
		## self.average_ads_blank, self.average_des_blank, self.diff_ads_blank, self.diff_des_blank
		##
		#Total Average computations
		#Asbsorption align
		refPressure = None
		aligned_ads_blank = []
		
		#Determine the reference
		if len(self.ads_blank) > 0:
			refPressure = []
			for index in range(len(self.ads_blank[0][0])):
				value = [val[0][index] for val in self.ads_blank]
				avg_value = sum(value)/len(self.ads_blank)
				refPressure.append(avg_value)

		#Align all the rest
<<<<<<< HEAD
		for index in range(len(self.ads_blank)):
			x1 = []
			x2 = []
			
			x1.extend(self.align(refPressure, self.ads_blank[index]))
=======
		for index in range(1, len(self.ads_blank)):
			x1 = []
			x2 = []

			x1.extend(self.align(refPressure, self.ads_blank[index]))
			x2.extend(self.align(refPressure, self.ads_blank[index], True))
>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
<<<<<<< HEAD
					
				else:
					pass
			aligned_ads_blank.append([refPressure, x1])
		
		aligned_average = []
		for index in range(len(aligned_ads_blank[0][1])):
			value = [val[1][index] for val in aligned_ads_blank]
			avg_value = sum(value)/len(aligned_ads_blank)
			aligned_average.append(avg_value)
		
		self.average_ads_blank = [refPressure, aligned_average]

=======
					for val in x2:
						pos = x2.index(val)
						if x2[pos] > 0:
							x1.append(x2[pos])
				else:
					pass
			aligned_ads_blank.append([refPressure, x1])
			
			#(pressure, concentration): [0], [1]
		self.average_ads_blank = [refPressure, self.average([data[1] for data in aligned_ads_blank])]

			
>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008
		#Desorbtion align
		refPressure = None
		aligned_des_blank = []
		
		#Determine the reference
		if len(self.des_blank) > 0:
			refPressure = []
			for index in range(len(self.des_blank[0][0])):
				value = [val[0][index] for val in self.des_blank]
				avg_value = sum(value)/len(self.des_blank)
				refPressure.append(avg_value)

		#Align all the rest
<<<<<<< HEAD
		for index in range(len(self.des_blank)):
			x1 = []
			x2 = []
			
			x1.extend(self.align(refPressure, self.des_blank[index], True))
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			aligned_des_blank.append([refPressure, x1])
		
		aligned_average = []
		for index in range(len(aligned_des_blank[0][1])):
			value = [val[1][index] for val in aligned_des_blank]
			avg_value = sum(value)/len(aligned_des_blank)
			aligned_average.append(avg_value)
		
		self.average_des_blank = [refPressure, aligned_average]
=======
		for index in range(1, len(self.des_blank)):
			x1 = []
			x2 = []

			x1.extend(self.align(refPressure, self.des_blank[index], True))
			x2.extend(self.align(refPressure, self.des_blank[index]))
			
			for val in x2:
				pos = x2.index(val)
				if x2[pos] < 0:
					del x2[pos]
					for val in x1:
						pos = x1.index(val)
						if x1[pos] > 0:
							x2.append(x1[pos])
				else:
					pass
			aligned_des_blank.append([refPressure, x2])
			
			#(pressure, concentration): [0], [1]
		self.average_des_blank = [refPressure, self.average([data[1] for data in aligned_des_blank])]
>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008

	
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
		
	
		# print "diff_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_ads_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_ads_blank"

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
						# self.des_blank[indexJ] as to be aligned.
<<<<<<< HEAD
						
=======

>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008
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
		refPressure= None
		aligned_ads_blank = []

		#Determine the reference
		if len(self.diff_ads_blank) > 0:
			refPressure = self.diff_ads_blank[0]['diff'][0]

		#Align all the rest
		for index in range(1, len(self.diff_ads_blank)):
			#(pressure, concentration): [0], [1]
			aligned_ads_blank.append([refPressure, self.align(refPressure, self.diff_ads_blank[index]['diff'])])

		self.average_diff_ads_blank = [refPressure, self.average([data[1] for data in aligned_ads_blank])]

		# print "average_diff_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.average_diff_ads_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_ads_blank"

		#Desorbtion align
		refPressure= None
		aligned_des_blank = []

		#Determine the reference
		if len(self.diff_des_blank) > 0:
			refPressure = self.diff_des_blank[0]['diff'][0]

		#Align all the rest
		for index in range(1, len(self.diff_des_blank)):
			#(pressure, concentration): [0], [1]
			aligned_des_blank.append([refPressure, self.align(refPressure, self.diff_des_blank[index]['diff'], True)])

		self.average_diff_des_blank = [refPressure, self.average([data[1] for data in aligned_des_blank])]

		# print "average_diff_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.average_diff_des_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_des_blank"

	

	def analyseAliq(self):
		##
		## self.average_ads_aliq, self.average_des_aliq, self.diff_ads_aliq, self.diff_des_aliq
		##
		#Total Average computations
		#Asbsorption align
		refPressure= None
		aligned_ads_aliq = []

		#Determine the reference
		if len(self.ads_aliq) > 0:
			refPressure = []
			for index in range(len(self.ads_aliq[0][0])):
				value = [val[0][index] for val in self.ads_aliq]
				avg_value = sum(value)/len(self.ads_aliq)
				refPressure.append(avg_value)

		#Align all the rest
<<<<<<< HEAD
		for index in range(len(self.ads_aliq)):
			x1 = []
			x2 = []
			
			x1.extend(self.align(refPressure, self.ads_aliq[index]))
=======
		for index in range(1, len(self.ads_aliq)):
			x1 = []
			x2 = []

			x1.extend(self.align(refPressure, self.ads_aliq[index]))
			x2.extend(self.align(refPressure, self.ads_aliq[index], True))
			print len(x1)
>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
<<<<<<< HEAD
					
				else:
					pass
			aligned_ads_aliq.append([refPressure, x1])
		
		aligned_average = []
		for index in range(len(aligned_ads_aliq[0][1])):
			value = [val[1][index] for val in aligned_ads_aliq]
			avg_value = sum(value)/len(aligned_ads_aliq)
			aligned_average.append(avg_value)
		
		self.average_ads_aliq = [refPressure, aligned_average]
=======
					for val in x2:
						pos = x2.index(val)
						if x2[pos] > 0:
							x1.append(x2[pos])
				else:
					pass
			aligned_ads_aliq.append([refPressure, x1])
			
			
			#(pressure, concentration): [0], [1]
		self.average_ads_aliq = [refPressure, self.average([data[1] for data in aligned_ads_aliq])]
>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008

		#Desorbtion align
		refPressure = None
		aligned_des_aliq = []
		
		#Determine the reference
		if len(self.des_aliq) > 0:
			refPressure = []
			for index in range(len(self.des_aliq[0][0])):
				value = [val[0][index] for val in self.des_aliq]
				avg_value = sum(value)/len(self.des_aliq)
				refPressure.append(avg_value)

		#Align all the rest
<<<<<<< HEAD
		for index in range(len(self.des_aliq)):
=======
		for index in range(1, len(self.des_aliq)):
			#(pressure, concentration): [0], [1]
>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008
			x1 = []
			x2 = []
			
			x1.extend(self.align(refPressure, self.des_aliq[index], True))
<<<<<<< HEAD
			
			for val in x1:
				pos = x1.index(val)
				if x1[pos] < 0:
					del x1[pos]
					
				else:
					pass
			aligned_des_aliq.append([refPressure, x1])
		
		aligned_average = []
		for index in range(len(aligned_des_aliq[0][1])):
			value = [val[1][index] for val in aligned_des_aliq]
			avg_value = sum(value)/len(aligned_des_aliq)
			aligned_average.append(avg_value)
		
		self.average_des_aliq = [refPressure, aligned_average]

=======
			x2.extend(self.align(refPressure, self.des_aliq[index]))
			print len(x1)
			for val in x2:
				pos = x2.index(val)
				if x2[pos] < 0:
					del x2[pos]
					for val in x1:
						pos = x1.index(val)
						if x1[pos] > 0:
							x2.append(x1[pos])
				else:
					pass
			aligned_des_aliq.append([refPressure, x2])
			
			#(pressure, concentration): [0], [1]
		self.average_des_aliq = [refPressure, self.average([data[1] for data in aligned_des_aliq])]
>>>>>>> 751597ef4341f73f7b250232a6182fac2d0db008

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
						# self.ads_aliq[indexJ] as to be aligned.

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
				

		# print "diff_ads_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_ads_aliq)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_ads_aliq"

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
						# Computing self.ads_aliq[indexI] - self.ads_aliq[indexJ]
						# self.ads_aliq[indexJ] as to be aligned.
						# Computing self.ads_aliq[indexI] - self.ads_aliq[indexJ]
						# self.ads_aliq[indexJ] as to be aligned.
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
			
		# print "diff_des_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.diff_des_aliq)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++diff_des_aliq"

		##
		#Average diff computations
		#Asbsorption align
		refPressure= None
		aligned_ads_aliq = []

		#Determine the reference
		if len(self.diff_ads_aliq) > 0:
			refPressure = self.diff_ads_aliq[0]['diff'][0]

		#Align all the rest
		for index in range(1, len(self.diff_ads_aliq)):
			#(pressure, concentration): [0], [1]
			aligned_ads_aliq.append([refPressure, self.align(refPressure, self.diff_ads_aliq[index]['diff'])])

		self.average_diff_ads_aliq = [refPressure, self.average([data[1] for data in aligned_ads_aliq])]

		#Desorbtion align
		refPressure= None
		aligned_des_aliq = []

		#Determine the reference
		if len(self.des_aliq) > 0:
			refPressure = self.diff_des_aliq[0]['diff'][0]

		#Align all the rest
		for index in range(1, len(self.diff_des_aliq)):
			#(pressure, concentration): [0], [1]
			aligned_des_aliq.append([refPressure, self.align(refPressure, self.diff_des_aliq[index]['diff'], True)])

		self.average_diff_des_aliq = [refPressure, self.average([data[1] for data in aligned_des_aliq])]

	# def analyseCombine(self): 

	


	def analyseAll(self):
		self.analyseAliq()
		self.analyseBlank()
		# self.analyseCombine()

		# Plot average blank ads and des
		# print "average_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.average_ads_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_ads_blank"

		# print "average_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.average_des_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_des_blank"

		# Plot average diff ads and des

		# print "average_diff_ads_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.average_diff_ads_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_ads_blank"

		# print "average_diff_des_blank+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.average_diff_des_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_diff_des_blank"

		# Plot blanks combinations and diff

		# print "blanks_and_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps([ {'blank1':self.ads_blank[diff['i']], 'blank2':self.ads_blank[diff['j']], 'diff':diff['diff']} for diff in self.diff_ads_blank])
		# print json.dumps([ {'blank1':self.des_blank[diff['i']], 'blank2':self.des_blank[diff['j']], 'diff':diff['diff']} for diff in self.diff_des_blank])
		# print "+++++++++++++++++++++++++++++++++++++++++++++++blanks_and_diffs"

		# Plot all the blanks diffs
		# print "blanks_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps([ diff['diff'] for diff in self.diff_ads_blank])
		# print json.dumps([ diff['diff'] for diff in self.diff_des_blank])
		# print "+++++++++++++++++++++++++++++++++++++++++++++++blanks_diffs"

		# Assessment1: Are the diffs zero?
		# Assessment2: if not zero, Are the diffs constant?
		# Assessment3: if not constant, Are the diff evolving? How? Can we quantify it?

		# Plot all the aliq diffs.
		# The machine error should be behind the variations of the diffs.
		# print "aliqs_and_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps([ {'aliq1':self.ads_aliq[diff['i']], 'aliq2':self.ads_aliq[diff['j']], 'diff':diff['diff']} for diff in self.diff_ads_aliq])
		# print json.dumps([ {'aliq1':self.des_aliq[diff['i']], 'aliq2':self.des_aliq[diff['j']], 'diff':diff['diff']} for diff in self.diff_des_aliq])
		# print "+++++++++++++++++++++++++++++++++++++++++++++++aliqs_and_diffs"
		# All the diff together compared to the average blanks
		# print "aliqs_diffs+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps([ diff['diff'] for diff in self.diff_ads_aliq])
		# print json.dumps(self.average_ads_blank)
		##
		# print json.dumps([ diff['diff'] for diff in self.diff_des_aliq])
		# print json.dumps(self.average_des_blank)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++aliqs_diffs"

		# Assessement4: Are the diffs of the aliq evolving the same way as the average of the blanks?
		# Correlation with the the previous 3 assessments. If the variation is constant then, the
		# evolution should be uniform and always the same for all aliq. The differences will not show anything.
		# Yet if the evolution is not uniform and the blanks diff is not constant then should all follow the same scheme.

		# +1: If blanks diff is constant: We can remove the blanks average from the aliq
		# and compare the aliq and correlated that they are closer to be the same then we can conclude 
		# by sharing the average blanks. And we can share a database of blanks that will always give back the average to all
		# scientists. The more blanks we have the more closer to the approximated blanks we have.

		# +2: If blanks diff is not constant: We should see that the aliqs diff and the blanks average evolve the same
		# way. Then we should quantify the blanks by approximating it and sharing it to all scientist also. Except this
		# case it is not a simple average but an approximation base on many variations.
		# Here we should also take out the approximated global blank from the aliq and confirm that all diffs tend be very close
		# to zeros.

		# We use here the average to correct the data because being constant or not or needing approximation,
		# substracted with the aliqs should eliminates differences residus.

		# Compute the 



		# Compute the corrected
		# for aliq in self.ads_aliq:
		# 	# d = diffJK
		# 	# upperQR = np.percentile(d, 75, interpolation='higher')
		# 	# lowerQR = np.percentile(d, 25, interpolation='lower')
		# 	# innerQR = upperQR - lowerQR
		# 	# limit = upperQR + (6*innerQR)

		# 	# problem = False
		# 	# for el in diffJK:
		# 	# 	if el > limit:
		# 	# 		problem = True

		# 	# if not problem:
				
		# 	aligned_average_ads_blank = self.align(aliq[0], self.average_ads_blank)
		# 	corrected_aliq = [aliq[0], self.diff(aliq[1], aligned_average_ads_blank)]
		# 	self.corrected_ads_aliq.append(corrected_aliq)

		# for aliq in self.des_aliq:
		# 	aligned_average_des_blank = self.align(aliq[0], self.average_des_blank, True)
		# 	corrected_aliq = [aliq[0], self.diff(aliq[1], aligned_average_des_blank)]
		# 	self.corrected_des_aliq.append(corrected_aliq)

		# # Computing the average corrected
		# refPressure= None
		# aligned_corrected_ads_aliq = []

		# if len(self.corrected_ads_aliq) > 0:
		# 	refPressure = self.corrected_ads_aliq[0][0]

		# for index in range(1, len(self.corrected_ads_aliq)):
		# 	aligned_corrected_ads_aliq.append([refPressure, self.align(refPressure, self.corrected_ads_aliq[index])])

		# self.average_corrected_ads_aliq = [refPressure, self.average([data[1] for data in aligned_corrected_ads_aliq])]

		# refPressure= None
		# aligned_corrected_des_aliq = []

		# if len(self.corrected_des_aliq) > 0:
		# 	refPressure = self.corrected_des_aliq[0][0]

		# for index in range(1, len(self.corrected_des_aliq)):
		# 	aligned_corrected_des_aliq.append([refPressure, self.align(refPressure, self.corrected_des_aliq[index], True)])

		# self.average_corrected_des_aliq = [refPressure, self.average([data[1] for data in aligned_corrected_des_aliq])]

		# print "corrected_ads_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.corrected_ads_aliq)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++corrected_ads_aliq"

		# print "corrected_des_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.corrected_des_aliq)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++corrected_des_aliq"

		# print "average_corrected_ads_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.average_corrected_ads_aliq)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_corrected_ads_aliq"

		# print "average_corrected_des_aliq+++++++++++++++++++++++++++++++++++++++++++++++"
		# print json.dumps(self.average_corrected_des_aliq)
		# print "+++++++++++++++++++++++++++++++++++++++++++++++average_corrected_des_aliq"

		# Finish analyse

