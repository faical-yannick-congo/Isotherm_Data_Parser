import numpy as np
import glob, os
import simplejson as json 
import re

class AMC_Analyse:
	def __init__(self):

		self.blanks = []
		self.aliqs = []


	def load(self):
		os.chdir(os.path.dirname(os.getcwd()))
		#Load blanks
		for file in glob.glob("AMC/Data_Files/JSON/json_blank/*.json"):
			content = None
			with open(file, "r") as blank_file:
				content = blank_file.read()
				raw = json.loads(content)
				filename = file.split("/")[-1].split(".")[0]
				stamp = filename.split("_")[0]
				shot = filename.split("_")[1]
				name = filename.split("_")[2]
				element = filename.split("_")[3]
				limit_temperature = filename.split("_")[4]
				limit_pressure = filename.split("_")[5]
				sample = filename.split("_")[6]
				machine = filename.split("_")[7]
				blocks = self.split(raw)
				self.addIn(self.blanks, name, stamp, sample, shot, element, limit_temperature, limit_pressure, blocks[0], blocks[1])
				# self.blanks.append({"name":name,"ads":blocks[0], "des":blocks[1]})

		#Load aliqs
		for file in glob.glob("AMC/Data_Files/JSON/json_aliq/*.json"):
			content = None
			with open(file, "r") as aliq_file:
				content = aliq_file.read()
				raw = json.loads(content)
				filename = file.split("/")[-1].split(".")[0]
				stamp = filename.split("_")[0]
				shot = filename.split("_")[1]
				name = filename.split("_")[2]
				element = filename.split("_")[3]
				limit_temperature = filename.split("_")[4]
				limit_pressure = filename.split("_")[5]
				sample = filename.split("_")[6]
				machine = filename.split("_")[7]
				blocks = self.split(raw)
				self.addIn(self.aliqs, name, stamp, sample, shot, element, limit_temperature, limit_pressure, blocks[0], blocks[1])
				# self.blanks.append({"name":name,"ads":blocks[0], "des":blocks[1]})

		# print json.dumps({"blanks":self.blanks,"aliqs":self.aliqs}, sort_keys=True, indent=4, separators=(',', ': '))

	def addIn(self, experiments, name, stamp, sample, shot, element, limit_temperature, limit_pressure, ads, des):
		found = False
		for exp in experiments:
			if exp["name"] == name:
				exp["raw_runs"].append({"sample":"%s_%s"%(sample,stamp), "ads":ads, "des":des})
				found = True
		if not found:
			experiments.append({"name":name, "stamp":stamp, "shot":shot, "element":element, "temperature":limit_temperature, "pressure":limit_pressure, "raw_runs":[{"sample":"%s_%s"%(sample,stamp), "ads":ads, "des":des}], "aligned_runs":[], "raw_diffs":[], "aligned_diffs":[], "aligned_average":{}})

		return found

	def split(self, raw):

		begin3 = 1

		pressure_list = []
		conc_list = []

		ads = content= raw["content"]["ads"]
		des = content= raw["content"]["des"]

		# print json.dumps(des, sort_keys=True, indent=4, separators=(',', ': '))

		pressure_list1 = []
		conc_list1 = []

		pressure_list2 = []
		conc_list2 = []
		
		for ele in ads:
			pressure_list1.append(ele["pressure"]["value"])
			# conc_list1.append(ele["concentration"]["value"])
			if ele["concentration"]["value"] >= 0:
				conc_list1.append(ele["concentration"]["value"])
			else:
				conc_list1.append(0.0)

		for ele in des:
			pressure_list2.append(ele["pressure"]["value"])
			# conc_list2.append(ele["concentration"]["value"])
			if ele["concentration"]["value"] >= 0:
				conc_list2.append(ele["concentration"]["value"])
			else:
				conc_list2.append(0.0)

		return [[pressure_list1, conc_list1], [pressure_list2, conc_list2]]

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

	def analyse(self):
		#Do blanks first
		self.blank_aligned = []
		self.blank_raw_diffs = []
		self.blank_aligned_diffs = []

		self.aliq_aligned = []
		self.aliq_raw_diffs = []
		self.aliq_aligned_diffs = []

		self.analyseList(self.blanks, self.blank_aligned, self.blank_raw_diffs, self.blank_aligned_diffs)
		self.analyseList(self.aliqs, self.aliq_aligned, self.aliq_raw_diffs, self.aliq_aligned_diffs)


		#Do aliqs next

	def analyseList(self, experiments, aligned, raw_diffs, aligned_diffs):
		##
		## self.average_DES_blank, self.average_des_blank, self.diff_DES_blank, self.diff_des_blank
		##
		#Total Average computations
		#Asbsorption align
	
		refPressure = None

		diffs = []
		
		#Problem here.
		#Determine the reference
		if len(experiments) > 0:
			refPressure = []

			ads_min = experiments[0]["raw_runs"][0]["ads"][0][0]
			ads_max = experiments[0]["raw_runs"][0]["ads"][0][len(experiments[0]["raw_runs"][0]["ads"][0])-1]
			
			des_min = experiments[0]["raw_runs"][0]["des"][0][len(experiments[0]["raw_runs"][0]["des"][0])-1]
			des_max = experiments[0]["raw_runs"][0]["des"][0][0]

			for index_experiment in range(len(experiments)):

				for run in experiments[index_experiment]["raw_runs"]:
					print "Min: %f - Max: %f"%(run["ads"][0][0], run["ads"][0][len(run["ads"][0])-1])
					if run["ads"][0][len(run["ads"][0])-1] < ads_max:
						ads_max = run["ads"][0][len(run["ads"][0])-1]
					if run["ads"][0][0] > ads_min:
						ads_min = run["ads"][0][0]

				for run in experiments[index_experiment]["raw_runs"]:
					print "Min: %f - Max: %f"%(run["des"][0][0], run["des"][0][len(run["des"][0])-1])
					if run["des"][0][len(run["des"][0])-1] > des_min:
						des_min = run["des"][0][len(run["des"][0])-1]
					if run["des"][0][0] < des_max:
						des_max = run["des"][0][0]

			print "Ads-Boundary: %f - : %f"%(ads_min, ads_max)
			print "Des-Boundary: %f - : %f"%(des_min, des_max)

			for index_experiment in range(len(experiments)):
				refPressure.append({"ads":[], "des":[]})
				for index_ads in range(len(experiments[index_experiment]["raw_runs"][0]["ads"][0])):
					value = []
					for run in experiments[index_experiment]["raw_runs"]:
						try:
							# value.append(run["ads"][0][index_ads])
							val = run["ads"][0][index_ads]
							if val >= 0.0:
								value.append(val)
							else:
								value.append(0.0)
						except:
							value.append(0.0)
					# value = [run["ads"][0][index_ads] for run in experiments[index_experiment]["raw_runs"]]
					# print value
					avg_value = sum(value)/len(experiments[index_experiment]["raw_runs"])
					# print avg_value
					if avg_value >= ads_min and avg_value <= ads_max:
						refPressure[index_experiment]["ads"].append(avg_value)

				for index_des in range(len(experiments[index_experiment]["raw_runs"][0]["des"][0])):
					# experiments[index_experiment]["raw_runs"]
					# print json.dumps(experiments[index_experiment]["raw_runs"], sort_keys=True, indent=4, separators=(',', ': '))
					value = []
					for run in experiments[index_experiment]["raw_runs"]:
						try:
							# value.append(run["des"][0][index_des])
							val = run["des"][0][index_des]
							if val >= 0.0:
								value.append(val)
							else:
								value.append(0.0)
						except:
							value.append(0.0)
					# value = [run["des"][0][index_des] for run in experiments[index_experiment]["raw_runs"]]
					avg_value = sum(value)/len(experiments[index_experiment]["raw_runs"])

					if avg_value >= des_min and avg_value <= des_max:
						refPressure[index_experiment]["des"].append(avg_value)

		# print json.dumps(refPressure, sort_keys=True, indent=4, separators=(',', ': ')) 
		
		#Align all the rest
		for index_experiment in range(len(experiments)):
			result_aligned = {"experiment":index_experiment, "ads":[], "des":[]}
			for index_run in range(len(experiments[index_experiment]["raw_runs"])):
				ads_Y = []
				des_Y = []
				
				ads_Y.extend(self.align(refPressure[index_experiment]["ads"], experiments[index_experiment]["raw_runs"][index_run]["ads"]))
				des_Y.extend(self.align(refPressure[index_experiment]["des"], experiments[index_experiment]["raw_runs"][index_run]["des"], True))
				
				# for val in ads_Y:
				# 	pos = ads_Y.index_run(val)
				# 	if ads_Y[pos] < 0:
				# 		del ads_Y[pos]
						
				# 	else:
				# 		pass
				
				# for val in des_Y:
				# 	pos = des_Y.index_run(val)
				# 	if des_Y[pos] < 0:
				# 		del des_Y[pos]
						
				# 	else:
				# 		pass

				experiments[index_experiment]["aligned_runs"].append({"sample":experiments[index_experiment]["raw_runs"][index_run]["sample"],"ads":[refPressure[index_experiment]["ads"], ads_Y],"des":[refPressure[index_experiment]["des"], des_Y]})
				# experiments[index_experiment]["aligned_runs"]["des"].append([refPressure[index_diffs]["des"], des_Y])

			# aligned.append(result_aligned) #


		##
		#Comabinatorial diff computations

		for experiment in experiments:

			diff = {"experiment":experiments.index(experiment), "diffs":[]}

			ads_line = [0 for x in xrange(len(experiment["raw_runs"]))]
			ads_already = [ads_line[:] for x in xrange(len(experiment["raw_runs"]))]

			des_line = [0 for x in xrange(len(experiment["raw_runs"]))]
			des_already = [des_line[:] for x in xrange(len(experiment["raw_runs"]))]

			ads_diff = []
			des_diff = []

			for indexI in range(0, len(experiment["raw_runs"])):
				for indexJ in range(0, len(experiment["raw_runs"])):

					if indexI == indexJ:
						# Do not compute same element case
						ads_already[indexI][indexJ] = 1
						ads_already[indexJ][indexI] = 1
					else:
						if ads_already[indexI][indexJ] == 1 or ads_already[indexJ][indexI] == 1:
						# Leave asymetric stuff for now. Later we could use it to average
						# for better approximation??? More dig is needed.
							ads_already[indexJ][indexI] = 1
							ads_already[indexI][indexJ] = 1
						else:
				
							# print x2
							interpolateK = self.align(experiment["raw_runs"][indexJ]["ads"][0], experiment["raw_runs"][indexI]["ads"])
							diffJK = self.diff(experiment["raw_runs"][indexJ]["ads"][1], interpolateK)
							
							
							# d = diffJK
							# upperQR = np.percentile(d, 75, interpolation='higher')
							# lowerQR = np.percentile(d, 25, interpolation='lower')
							# innerQR = upperQR - lowerQR
							# limit = upperQR + (6*innerQR)

							# problem = False
							# for el in diffJK:
							# 	if el > limit:
							# 		problem = True

							# if not problem:
							ads_diff.append({'i':indexI, 'j':indexJ, 'diff':[experiment["raw_runs"][indexJ]["ads"][0], diffJK]})
							ads_already[indexI][indexJ] = 1
							# else:
							# 	print "Experiment %s : Problem ads with %s and %s"%(experiments.index(experiment), experiment["raw_runs"][indexI]["sample"],experiment["raw_runs"][indexJ]["sample"])

			for indexI in range(0, len(experiment["raw_runs"])):
				for indexJ in range(0, len(experiment["raw_runs"])):

					if indexI == indexJ:
						# Do not compute same element case
						des_already[indexI][indexJ] = 1
						des_already[indexJ][indexI] = 1
					else:
						if des_already[indexI][indexJ] == 1 or des_already[indexJ][indexI] == 1:
						# Leave asymetric stuff for now. Later we could use it to average
						# for better approximation??? More dig is needed.
							des_already[indexJ][indexI] = 1
							des_already[indexI][indexJ] = 1
						else:
				
							# print x2
							interpolateK = self.align(experiment["raw_runs"][indexJ]["des"][0], experiment["raw_runs"][indexI]["des"], True)
							diffJK = self.diff(experiment["raw_runs"][indexJ]["des"][1], interpolateK)
							
							
							# d = diffJK
							# upperQR = np.percentile(d, 75, interpolation='higher')
							# lowerQR = np.percentile(d, 25, interpolation='lower')
							# innerQR = upperQR - lowerQR
							# limit = upperQR + (6*innerQR)

							# problem = False
							# for el in diffJK:
							# 	if el > limit:
							# 		problem = True

							# if not problem:
							des_diff.append({'i':indexI, 'j':indexJ, 'diff':[experiment["raw_runs"][indexJ]["des"][0], diffJK]})
							des_already[indexI][indexJ] = 1
							# else:
							# 	print "Experiment %s : Problem des with %s and %s"%(experiments.index(experiment), experiment["raw_runs"][indexI]["sample"],experiment["raw_runs"][indexJ]["sample"])

			for diff_index in range(len(ads_diff)):
				diff["diffs"].append({"i":des_diff[diff_index]["i"], "j":des_diff[diff_index]["j"],"ads":ads_diff[diff_index], "des":des_diff[diff_index]})
				raw_diff = {"i":"", "j":"", "ads":[], "des":[]}
				raw_diff["ads"] = ads_diff[diff_index]["diff"]
				raw_diff["des"] = des_diff[diff_index]["diff"]		
				raw_diff["i"] = experiment["raw_runs"][des_diff[diff_index]["i"]]["sample"]
				raw_diff["j"] = experiment["raw_runs"][des_diff[diff_index]["j"]]["sample"]

				experiment["raw_diffs"].append(raw_diff)

			diffs.append(diff) #
			# raw_diffs.append(raw_diff)
		
		
		##
		#Average diff computations
		#Asbsorption align

		if len(diffs) > 0:
			refPressure = []

			for index_diff in range(len(diffs)):
				refPressure.append({"ads":[], "des":[]})
				# print diffs
				for index_ads in range(len(diffs[index_diff]["diffs"][0]["ads"]["diff"][0])):
					value = []
					for comparison in diffs[index_diff]["diffs"]:
						try:
							value.append(comparison["ads"]["diff"][0][index_ads])
						except:
							value.append(0.0)
					avg_value = sum(value)/len(diffs[index_diff]["diffs"])
					refPressure[index_diff]["ads"].append(avg_value)

				for index_ads in range(len(diffs[index_diff]["diffs"][0]["des"]["diff"][0])):
					# value = [comparison["des"]["diff"][0][index_ads] for comparison in diffs[index_diff]["diffs"]]
					value = []
					for comparison in diffs[index_diff]["diffs"]:
						try:
							value.append(comparison["des"]["diff"][0][index_ads])
						except:
							value.append(0.0)
					avg_value = sum(value)/len(diffs[index_diff]["diffs"])
					refPressure[index_diff]["des"].append(avg_value)


		for diff in diffs:
			#Align all the rest
			index_diffs = diffs.index(diff)
			result_aligned = {"experiment":diff["experiment"], "ads":[], "des":[], "average_ads":[], "average_des":[]}
			for index_diff in range(len(diff["diffs"])):
				ads_Y = []
				des_Y = []
				
				ads_Y.extend(self.align(refPressure[index_diffs]["ads"], diff["diffs"][index_diff]["ads"]["diff"]))
				result_aligned["ads"].append([refPressure[index_diffs]["ads"], ads_Y])

				des_Y.extend(self.align(refPressure[index_diffs]["des"], diff["diffs"][index_diff]["des"]["diff"], True))
				result_aligned["des"].append([refPressure[index_diffs]["des"], des_Y])

				aligned_diff = {"i":"", "j":"", "ads":[], "des":[]}
				aligned_diff["ads"] = [refPressure[index_diffs]["ads"], ads_Y]
				aligned_diff["des"] = [refPressure[index_diffs]["des"], des_Y]		
				aligned_diff["i"] = experiments[diff["experiment"]]["raw_runs"][diff["diffs"][index_diff]["i"]]["sample"]
				aligned_diff["j"] = experiments[diff["experiment"]]["raw_runs"][diff["diffs"][index_diff]["j"]]["sample"]

				experiments[diff["experiment"]]["aligned_diffs"].append(aligned_diff)

			average_ads = []
			for index in range(len(result_aligned["ads"][0][1])):
				value = [val[1][index] for val in result_aligned["ads"]]
				avg_value = sum(value)/len(result_aligned["ads"])
				average_ads.append(avg_value)
			result_aligned["average_ads"].append([refPressure[index_diffs]["ads"], average_ads])

			average_des = []
			for index in range(len(result_aligned["des"][0][1])):
				value = [val[1][index] for val in result_aligned["des"]]
				avg_value = sum(value)/len(result_aligned["des"])
				average_des.append(avg_value)
			result_aligned["average_des"].append([refPressure[index_diffs]["des"], average_des])

			experiments[diff["experiment"]]["aligned_average"] = {"ads":[refPressure[index_diffs]["ads"], average_ads], "des":[refPressure[index_diffs]["des"], average_des]}

			# aligned_diffs.append(result_aligned)#


	def analyseAll(self):
		self.analyse()
		# self.analyseAliq()