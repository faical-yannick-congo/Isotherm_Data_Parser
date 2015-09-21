### Script for file format conversion for AMC (machine 3) ####

import glob, os
import posixpath as path
import xlrd
from collections import OrderedDict
import simplejson as json 
import pprint
import tkFileDialog
from Tkinter import *	
# import dicttoxml
import lxml.etree as etree
import traceback
import xmltodict

def isAbsorbed(content):
	if len(content) > 0:
		if content[-1]["measured pressure"]["value"] >= content[0]["measured pressure"]["value"]:
			return True
		else:
			return False
	else:
		print "Error: Dataset might be empty."
		return True

def load_set(file_path):
	wb1 = xlrd.open_workbook(filename = file_path)
	sh1 = wb1.sheet_by_index(0)

	content = []

	begin = 0

	while True: 
		try: 
			row1 = {}

			row1["index"] = begin
			
			row1["serial"] = {}
			row1["serial"]["unit"] = ""
			row1["serial"]["value"] = sh1.cell_value(begin, 0)

			row1["time"] = {}
			row1["time"]["unit"] = "s (seconds)"
			row1["time"]["value"] = sh1.cell_value(begin, 1)

			row1["sample_temp"] = {} 
			row1["sample_temp"]["unit"] = "C"
			row1["sample_temp"]["value"] = sh1.cell_value(begin, 2)

			row1["pressure"] = {}
			row1["pressure"]["unit"] = "bar"
			row1["pressure"]["value"] = (sh1.cell_value(begin, 3))/(0.9869)

			row1["volume"] = {}
			row1["volume"]["unit"] = "L"
			row1["volume"]["value"] = sh1.cell_value(begin, 4)/1000

			row1["concentration"] = {}
			row1["concentration"]["unit"] = "mmol/g"
			row1["concentration"]["value"] = (sh1.cell_value(begin, 5)*10)/44

			content.append(row1)
			begin += 1 

		except: 
			# traceback.print_exc()
			break 

	return content


if __name__ == '__main__':

	os.chdir(os.path.dirname(os.getcwd()))

	already = []
	
	for file in glob.glob("AMC/Data_Files/Excel/*.xlsx"):
		absorb_path = ""
		desorb_path = ""

		if file.split("/")[-1] in already:
			pass
		else:

			sequence1 = file.split("/")[-1].split("_")[0]
			sequence2 = file.split("/")[-1].split("_")[1]
			sequence3 = file.split("/")[-1].split("_")[2]
			sequence4 = file.split("/")[-1].split("_")[3]
			sequence5 = file.split("/")[-1].split("_")[4]
			sequence6 = file.split("/")[-1].split("_")[5]
			sequence7 = file.split("/")[-1].split("_")[6]
			sequence8 = file.split("/")[-1].split("_")[7]

			found = -1
			order = -1

			# print sequence7

			if "ads" in file:
				found = 0
				order = int(sequence7.split("ads")[0])
				absorb_path = file
				desorb_path = "%s%ddes_AMC.xlsx"%(absorb_path.split(sequence7)[0], order+1)
				filename = "%s_%s_%s_%s_%s_%s_%d"%(sequence1, sequence2, sequence3, sequence4, sequence5, sequence6, order)
			else:
				found = 1
				order = int(sequence7.split("des")[0])
				desorb_path = file
				absorb_path = "%s%dads_AMC.xlsx"%(desorb_path.split(sequence7)[0], order-1)
				filename = "%s_%s_%s_%s_%s_%s_%d"%(sequence1, sequence2, sequence3, sequence4, sequence5, sequence6, order-1)

			absorb_content = load_set(absorb_path)
			desorb_content = load_set(desorb_path)

			# print json.dumps(desorb_content, sort_keys=True, indent=4, separators=(',', ': '))

			excelPath = '%s_AMC.xlsx'%filename
			jsonPath = '%s_AMC.json'%filename
			xmlPath = '%s_AMC.xml'%filename

			AMC_Data = {"dataset":excelPath, "header":{}, "content":{}}

			AMC_Data["header"]["absorbate"] = sequence4
			AMC_Data["header"]["filename"] = excelPath.split(".")[0]
			AMC_Data["header"]["notes"] = ""
			AMC_Data["header"]["operator"] = ""
			AMC_Data["header"]["experiment"] = {"id":order, "name":"%s %s %s"%(sequence2, sequence4, sequence3), "started":sequence1}
			AMC_Data["header"]["sample"] = {"lot":"%s_%s_%s with %s"%(sequence2, sequence3, sequence4, sequence5), "name":"%s pressure up to %s"%(sequence2, sequence5)}

			AMC_Data["content"]["ads"] = absorb_content
			AMC_Data["content"]["des"] = desorb_content

			if "SiShot" in file:#Blanks
				with open('AMC/Data_Files/JSON/json_blank/%s'%jsonPath, 'w') as f:
					f.write(json.dumps(AMC_Data, sort_keys=True, indent=4, separators=(',', ': ')))
						
				with open('AMC/Data_Files/XML/xml_blank/%s'%xmlPath, 'w') as f:
					# f.write(dicttoxml.dicttoxml(AMC_Data))
					f.write(xmltodict.unparse({"amc":AMC_Data}))

				x = etree.parse("AMC/Data_Files/XML/xml_blank/%s"%xmlPath)

				with open('AMC/Data_Files/XML/xml_blank/%s'%xmlPath, 'w') as f:
					f.write(etree.tostring(x, pretty_print = True))
			else:#Aliqs

				with open('AMC/Data_Files/JSON/json_aliq/%s'%jsonPath, 'w') as f:
					f.write(json.dumps(AMC_Data, sort_keys=True, indent=4, separators=(',', ': ')))
						
				with open('AMC/Data_Files/XML/xml_aliq/%s'%xmlPath, 'w') as f:
					# f.write(dicttoxml.dicttoxml(AMC_Data))
					f.write(xmltodict.unparse({"amc":AMC_Data}))

				x = etree.parse("AMC/Data_Files/XML/xml_aliq/%s"%xmlPath)

				with open('AMC/Data_Files/XML/xml_aliq/%s'%xmlPath, 'w') as f:
					f.write(etree.tostring(x, pretty_print = True))

			already.append(absorb_path.split("/")[-1])
			already.append(desorb_path.split("/")[-1])
		
	print "done" 

