#### Script for file format conversion for IGA (machine 2) ####

import glob, os
import xlrd
from collections import OrderedDict
import simplejson as json 
import pprint
import tkFileDialog
from Tkinter import *	
# import dicttoxml
import lxml.etree as etree
import os.path
import xmltodict

if __name__ == '__main__':

	os.chdir(os.path.dirname(os.getcwd()))
	# print "Starting... %s"%os.getcwd()
	for file in glob.glob("IGA/Data_Files/Excel/*.xlsx"):
		file_path = file

		# print "File %s..."%file_path

		sequence1 = file_path.split("/")[-1].split("_")[0]
		sequence2 = file_path.split("/")[-1].split("_")[1]
		sequence3 = file_path.split("/")[-1].split("_")[2]
		sequence4 = file_path.split("/")[-1].split("_")[3]
		sequence5 = file_path.split("/")[-1].split("_")[4]
		sequence6 = file_path.split("/")[-1].split("_")[5]
		sequence7 = file_path.split("/")[-1].split("_")[6].split(".")[0]

		sequence = file.split("/")[-1].split("_")[0]
		wb = xlrd.open_workbook(filename = file_path)
		sh = wb.sheet_by_index(0)

		IGA_Data = {"dataset":file_path.split("/")[-1]}

		IGA_Header = {}
		IGA_Content = []

		#### 6/28/2015 Discussing what the header should contain ####

		IGA_Data["header"] = IGA_Header

		#### Content ####

		begin = 1

		W_init = 0

		while 1: 
			try: 
				row = {}

				row["index"] = begin 

				row["weights"] = []
				row["weights"].append({"prefix":"", "unit":"mg", "value": sh.cell_value(begin, 0)})
				row["weights"].append({"prefix":"", "unit":"%% chg", "value": sh.cell_value(begin, 2)})

				row["pressure"] = {}
				row["pressure"]["unit"] = "Bar"
				row["pressure"]["value"] = (sh.cell_value(begin, 1))/1000

				if "SiShot" in file_path: # In case of blank: mg Already the first value
					row["concentration"] = {}
					row["concentration"]["unit"] = "mg"
					if row["index"] == 1:
						W_init = sh.cell_value(begin, 0)
					row["concentration"]["value"] = sh.cell_value(begin, 0) - W_init
				else: # In case of aliq: w% => mmol/g.
					# We already have it but in case of an updated: (sh.cell_value(begin, 4)*10)/44
					row["concentration"] = {}
					row["concentration"]["unit"] = "mmol/g"
					row["concentration"]["value"] = sh.cell_value(begin, 3)

				row["sample_temp"] = {}
				row["sample_temp"]["unit"] = "C"
				row["sample_temp"]["value"] = sh.cell_value(begin, 4)

				IGA_Content.append(row)
				begin += 1 

			except: 
				break 

		IGA_Data["content"] = IGA_Content 

		#filename = file_path.split("/")[-1].split(".")[0]

		if sequence2 == "SiShot": #Blank
			jsonPath = '%s_IGA.json'%file_path.split("/")[-1].split(".")[0]
			xmlPath = '%s_IGA.xml'%file_path.split("/")[-1].split(".")[0]
			IGA_Data["header"]["absorbate"] = sequence3
			IGA_Data["header"]["filename"] = file_path.split("/")[-1].split(".")[0]
			IGA_Data["header"]["notes"] = ""
			IGA_Data["header"]["operator"] = ""
			IGA_Data["header"]["experiment"] = {"id":"", "name":"%s %s %s"%(sequence3, sequence6, sequence7), "started":sequence1}
			IGA_Data["header"]["sample"] = {"lot":"%s with %s"%(sequence7, sequence4), "name":"%s pressure up to %s"%(sequence2, sequence5)}
			
			with open('IGA/Data_Files/JSON/json_blank/%s'%jsonPath, 'w') as f:
				f.write(json.dumps(IGA_Data, sort_keys=True, indent=4, separators=(',', ': ')))
					
			with open('IGA/Data_Files/XML/xml_blank/%s'%xmlPath, 'w') as f:
				# f.write(dicttoxml.dicttoxml(IGA_Data))
				f.write(xmltodict.unparse({"iga":IGA_Data}))

			x = etree.parse("IGA/Data_Files/XML/xml_blank/%s"%xmlPath)

			with open('IGA/Data_Files/XML/xml_blank/%s'%xmlPath, 'w') as f:
				f.write(etree.tostring(x, pretty_print = True))
		else: #Aliq
			jsonPath = '%s.json'%file_path.split("/")[-1].split(".")[0]
			xmlPath = '%s.xml'%file_path.split("/")[-1].split(".")[0]
			IGA_Data["header"]["absorbate"] = sequence2
			IGA_Data["header"]["filename"] = file_path.split("/")[-1].split(".")[0]
			IGA_Data["header"]["notes"] = ""
			IGA_Data["header"]["operator"] = ""
			IGA_Data["header"]["experiment"] = {"id":"", "name":"%s %s %s"%(sequence2, sequence5, sequence6), "started":sequence1}
			IGA_Data["header"]["sample"] = {"lot":"%s with %s"%(sequence6, sequence3), "name":"Unknown pressure up to %s"%(sequence4)}
			
			with open('IGA/Data_Files/JSON/json_aliq/%s'%jsonPath, 'w') as f:
				f.write(json.dumps(IGA_Data, sort_keys=True, indent=4, separators=(',', ': ')))
					
			with open('IGA/Data_Files/XML/xml_aliq/%s'%xmlPath, 'w') as f:
				# f.write(dicttoxml.dicttoxml(IGA_Data))
				f.write(xmltodict.unparse({"iga":IGA_Data}))

			x = etree.parse("IGA/Data_Files/XML/xml_aliq/%s"%xmlPath)

			with open('IGA/Data_Files/XML/xml_aliq/%s'%xmlPath, 'w') as f:
				f.write(etree.tostring(x, pretty_print = True))

	print "done"









