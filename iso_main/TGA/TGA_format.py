# -*- coding: ascii -*-

import glob, os
import xlrd
from collections import OrderedDict
import simplejson as json 
import pprint
import tkFileDialog
import tkSimpleDialog
from Tkinter import *	
# import dicttoxml
import lxml.etree as etree
import traceback
import xmltodict

class TGApp:

	def __init__(self):

		os.chdir(os.path.dirname(os.getcwd()))


	def load_sheet(self, file_path):
		print "Formatting %s..."%file_path
		for index in [1, 3, 4]:
			sheet = index
			print "Sheet No: %s"%(sheet)
			try:
				wb = xlrd.open_workbook(filename = file_path)
				sh = wb.sheet_by_index(int(sheet))
				self.runJSON(file_path, sh, sheet)
			except:
				traceback.print_exc()
			# self.button2 = Button(self.root, text = "Init File Conversion", command = self.runJSON)
			# self.button2.pack()
		# self.button.destroy()

	def run(self):
		for file in glob.glob("TGA/Data_Files/Excel_samples/*.xlsx"):
			self.load_sheet(file)
		# print "Please select a file"
		# self.file_path = tkFileDialog.askopenfilename()
		# self.wb = xlrd.open_workbook(filename = self.file_path)
		# self.file = self.file_path 
		
		# self.root.mainloop()
			

	def runJSON(self, file_path, sh, sheet):
		already = []

		TGA_Data = {"dataset":file_path.split("/")[-1]}

		TGA_Header = {}
		TGA_Content = []

		#FileName
		TGA_Header["filename"] = sh.cell_value(0, 2)

		#Experiment
		TGA_Header["experiment"] = {}
		TGA_Header["experiment"]["name"]= sh.cell_value(1, 2)
		TGA_Header["experiment"]["id"]= sh.cell_value(3, 2)
		TGA_Header["experiment"]["started"]= sh.cell_value(18, 2)

		#Operator
		TGA_Header["operator"] = sh.cell_value(2, 2)

		#Sample Name
		TGA_Header["sample"] = {}
		TGA_Header["sample"]["name"] = sh.cell_value(4, 2)
		TGA_Header["sample"]["lot"] = sh.cell_value(5, 2)

		#Notes
		TGA_Header["notes"] = sh.cell_value(6, 2)

		#Pump
		TGA_Header["pump"] = sh.cell_value(7, 3)

		#Absorbate
		TGA_Header["absorbate"] = sh.cell_value(8, 2)

		#Temp
		TGA_Header["temperature"] = {}
		TGA_Header["temperature"]["drying"] = sh.cell_value(9, 2)
		TGA_Header["temperature"]["run"] = {}
		TGA_Header["temperature"]["run"]["value"] = sh.cell_value(13, 2)
		TGA_Header["temperature"]["run"]["unit"] = sh.cell_value(13, 3).encode('ascii', 'ignore') 

		#Heating Rate
		TGA_Header["heating_rate"] = {}
		TGA_Header["heating_rate"]["value"] = sh.cell_value(10, 2)
		TGA_Header["heating_rate"]["unit"] = sh.cell_value(10, 3).encode('ascii', 'ignore') 

		#Max Time
		TGA_Header["max_time"] = {}
		TGA_Header["max_time"]["drying"] = {}
		TGA_Header["max_time"]["drying"]["value"] = sh.cell_value(11, 2)
		TGA_Header["max_time"]["drying"]["unit"] = sh.cell_value(11, 3).encode('ascii', 'ignore')
		TGA_Header["max_time"]["equil"] = {}
		TGA_Header["max_time"]["equil"]["value"] = sh.cell_value(14, 2)
		TGA_Header["max_time"]["equil"]["unit"] = sh.cell_value(14, 3).encode('ascii', 'ignore') 

		#Equal Crit
		TGA_Header["equil_crit"] = []

		equil_1 = {}
		equil_1["value1"] = sh.cell_value(12, 2)
		equil_1["unit1"] = sh.cell_value(12, 3).encode('ascii', 'ignore') 
		equil_1["value2"] = sh.cell_value(12, 4)
		equil_1["unit2"] = sh.cell_value(12, 5).encode('ascii', 'ignore') 

		equil_2 = {}
		equil_2["value1"] = sh.cell_value(15, 2)
		equil_2["unit1"] = sh.cell_value(15, 3).encode('ascii', 'ignore') 
		equil_2["value2"] = sh.cell_value(15, 4)
		equil_2["unit2"] = sh.cell_value(15, 5).encode('ascii', 'ignore')

		TGA_Header["equil_crit"].append(equil_1)
		TGA_Header["equil_crit"].append(equil_2)


		#Pres Steps
		steps = sh.cell_value(16, 2)[1:len(sh.cell_value(16, 2))-1]
		TGA_Header["pressure_steps"] = steps.split(",")

		#Data Logging Interval
		TGA_Header["data_logging_interval"] = {}
		TGA_Header["data_logging_interval"]["value1"] = sh.cell_value(17, 2)
		TGA_Header["data_logging_interval"]["unit1"] = sh.cell_value(17, 3).encode('ascii', 'ignore') 
		TGA_Header["data_logging_interval"]["value2"] = sh.cell_value(17, 4)
		TGA_Header["data_logging_interval"]["unit2"] = sh.cell_value(17, 5).encode('ascii', 'ignore') 

		#Run Started
		TGA_Header["run_started"] = sh.cell_value(19, 2)

		TGA_Data["header"] = TGA_Header


		#Content

		begin = 23

		# print str(begin)
		# print sh.cell_value(23, 0)

		while 1:
			try:
				row = {}

				row["index"] = begin -22
				row["elap_time"] = {}
				row["elap_time"]["unit"] = sh.cell_value(22, 0).encode('ascii', 'ignore') 
				row["elap_time"]["value"] = sh.cell_value(begin, 0)

				row["weights"] = []
				weight1 = {}
				weight1["prefix"] = ""
				weight1["unit"] = sh.cell_value(22, 1).encode('ascii', 'ignore') 
				weight1["value"] = sh.cell_value(begin, 1)
				row["weights"].append(weight1)

				weight2 = {}
				weight2["prefix"] = ""
				weight2["unit"] = sh.cell_value(22, 2).encode('ascii', 'ignore') 
				weight2["value"] = sh.cell_value(begin, 2)
				row["weights"].append(weight2)

				weight3 = {}
				weight3["prefix"] = "Corr."
				weight3["unit"] = sh.cell_value(22, 7).encode('ascii', 'ignore') 
				weight3["value"] = sh.cell_value(begin, 7)
				row["weights"].append(weight3)

				weight4 = {}
				weight4["prefix"] = "Corr."
				weight4["unit"] = sh.cell_value(22, 8).encode('ascii', 'ignore') 
				weight4["value"] = sh.cell_value(begin, 8)
				row["weights"].append(weight4)

				weight5 = {}
				weight5["prefix"] = ""
				weight5["unit"] = "mass change(mg)"
				weight5["value"] = ((sh.cell_value(begin, 8))*(sh.cell_value(23, 7)))/100
				row["weights"].append(weight5)

				row["pressure"] = {}
				row["pressure"]["unit"] = "Bar"
				row["pressure"]["value"] = (sh.cell_value(begin, 3))/(750.1)

				row["sample_temp"] = {}
				row["sample_temp"]["unit"] = sh.cell_value(22, 4).encode('ascii', 'ignore') 
				row["sample_temp"]["value"] = sh.cell_value(begin, 4)

				row["Z"] = {}
				row["Z"]["unit"] = sh.cell_value(22, 6).encode('ascii', 'ignore') 
				row["Z"]["value"] = sh.cell_value(begin, 6)

				TGA_Content.append(row)
				begin += 1
			except:
				# traceback.print_exc()
				break


		#End content
		TGA_Data["content"] = TGA_Content
		
		sequence1 = file_path.split("/")[-1].split("_")[0]
		sequence2 = "sheet%s"%(sheet + 1)
		sequence3 = file_path.split("/")[-1].split("_")[1]
		sequence4 = file_path.split("/")[-1].split("_")[2]
		sequence5 = file_path.split("/")[-1].split("_")[5]
		sequence6 = file_path.split("/")[-1].split("_")[6].split(".")[0]
		


		# print sequence1
		# print sequence2
		# print sequence3
		# print sequence4
		# print sequence5
		excelPath = '%s_%s_%s_%s_CO2_20C_%s_%s.xlsx'%(sequence1, sequence2, sequence3, 
														     sequence4, sequence5, sequence6)
		jsonPath = '%s_%s_%s_%s_CO2_20C_%s_%s.json'%(sequence1, sequence2, sequence3, 
													    sequence4, sequence5, sequence6)
		xmlPath = '%s_%s_%s_%s_CO2_20C_%s_%s.xml'%(sequence1, sequence2, sequence3, 
													  sequence4, sequence5, sequence6)
		
		if sequence1 and sequence2 and sequence3 and sequence4 and\
						 sequence5 and sequence6 in already:
			pass

		elif sequence6 == 'TGA-bad':
			with open('TGA/Data_Files/JSON/json_bad/%s'%jsonPath, 'w') as f:
				f.write(json.dumps(TGA_Data, sort_keys=True, indent=4, separators=(',', ': ')))

			with open('TGA/Data_Files/XML/xml_bad/%s'%xmlPath, 'w') as f:
				# f.write(dicttoxml.dicttoxml(TGA_Data))
				f.write(xmltodict.unparse({"tga":TGA_Data}))

			x = etree.parse("TGA/Data_Files/XML/xml_bad/%s"%xmlPath)

			with open('TGA/Data_Files/XML/xml_bad/%s'%xmlPath, 'w') as f:
				f.write(etree.tostring(x, pretty_print = True))	

		elif sequence3 == 'SiShot':
			with open('TGA/Data_Files/JSON/json_blank/%s'%jsonPath, 'w') as f:
				f.write(json.dumps(TGA_Data, sort_keys=True, indent=4, separators=(',', ': ')))

			with open('TGA/Data_Files/XML/xml_blank/%s'%xmlPath, 'w') as f:
				# f.write(dicttoxml.dicttoxml(TGA_Data))
				f.write(xmltodict.unparse({"tga":TGA_Data}))

			x = etree.parse("TGA/Data_Files/XML/xml_blank/%s"%xmlPath)

			with open('TGA/Data_Files/XML/xml_blank/%s'%xmlPath, 'w') as f:
				f.write(etree.tostring(x, pretty_print = True))	

		else:

			with open('TGA/Data_Files/JSON/json_aliq/%s'%jsonPath, 'w') as f:
				f.write(json.dumps(TGA_Data, sort_keys=True, indent=4, separators=(',', ': ')))

			with open('TGA/Data_Files/XML/xml_aliq/%s'%xmlPath, 'w') as f:
				# f.write(dicttoxml.dicttoxml(TGA_Data))
				f.write(xmltodict.unparse({"tga":TGA_Data}))

			x = etree.parse("TGA/Data_Files/XML/xml_aliq/%s"%xmlPath)

			with open('TGA/Data_Files/XML/xml_aliq/%s'%xmlPath, 'w') as f:
				f.write(etree.tostring(x, pretty_print = True))	

			already.append(sequence1)
			already.append(sequence2)
			already.append(sequence3)
			already.append(sequence4)	
			already.append(sequence5)


if __name__ == '__main__':

	TGInstance = TGApp()
	TGInstance.run()
	
	print "done"




			