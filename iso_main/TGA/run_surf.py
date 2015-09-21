from TGA_analyse_aliq2 import TGA_AnalyseAliq2
# from TGA_analyse_aliq3 import TGA_AnalyseAliq3
import simplejson as json 
from TGA_plot_surf import TGA_Plot
import numpy as np


if __name__ == '__main__':
	analyse = TGA_AnalyseAliq2()
	# analyse3 = TGA_AnalyseAliq3()
	analyse.load()
	analyse.analyseAll()
	# analyse3.load()
	# analyse3.analyseAll()
	plot = TGA_Plot()

############################################# Simple plots #############################################

# w/ blank subtraction 

# plot.aliqSimplePlot(analyse.ADS_aliqBlank1_list, analyse.DES_aliqBlank1_list, 'aliq2_blank1_corr', 'Adsorption',\
# 													'Desorption', xmax = 45, ymax = 20, yAxisLabel = 'delta mass (mg)')

# plot.aliqSimplePlot(analyse.ADS_aliqBlank2_list, analyse.DES_aliqBlank2_list, 'aliq2_blank2_corr', 'Adsorption',\
# 													'Desorption', xmax = 45, ymax = 20, yAxisLabel = 'delta mass (mg)')


# # w/o blank subtraction 

# plot.aliqSimplePlot(analyse.ADS_aliqRaw_list, analyse.DES_aliqRaw_list, 'aliq2_raw', 'Adsorption',\
# 													'Desorption', xmax = 45, ymax = 20, yAxisLabel = 'delta mass (mg)')

# ############################################# Many plots #############################################

# # compare aliq difference between raw, corected1, and corrected2

# plot.ads_aliqDiffPlot(analyse.ADSaliqBlank_compareAll_list[0], analyse.ADSaliqBlank_compareAll_list[1],\
# 					  analyse.ADSaliqBlank_compareAll_list[2], 'ADSraw_blank_comparison', 0, 'aliqRaw_aliqBlank1_diff',\
# 					  'aliqRaw_aliqBlank2_diff', 'aliqBlank1_aliqBlank2_diff', xmax = 45, ymin = -0.03, ymax = 0.10)

# plot.des_aliqDiffPlot(analyse.DESaliqBlank_compareAll_list[0], analyse.DESaliqBlank_compareAll_list[1],\
# 					  analyse.DESaliqBlank_compareAll_list[2], 'DESraw_blank_comparison', 0, 'aliqRaw_aliqBlank1_diff',\
# 					  'aliqRaw_aliqBlank2_diff', 'aliqBlank1_aliqBlank2_diff', xmax = 45, ymin = -0.03, ymax = 0.15)

# compare all blanks with average 

plot.ads_blankManyPlot(analyse.ADSblank1_compareAll_list, 'ADScompare_all_blanks_1', xmax = 45,  ymax = 0.2)

plot.des_blankManyPlot(analyse.DESblank1_compareAll_list, 'DEScompare_all_blanks_1', xmax = 45,  ymax = 0.2)

plot.ads_blankManyPlot(analyse.ADSblank2_compareAll_list, 'ADScompare_all_blanks_2', xmax = 45,  ymax = 0.2)

plot.des_blankManyPlot(analyse.DESblank2_compareAll_list, 'DEScompare_all_blanks_2', xmax = 45,  ymax = 0.2)

############################################# Diff plots #############################################

plot.ads_blankDiffPlot(analyse.ADS_blank1_diff_list, analyse.ADS_blank2_diff_list, analyse.ADS_blankDiff_list, 'blanks_diffs_ads',\
																				'Difference between lines', legendOne="blank1_Ads_average", legendTwo="blank2_Ads_average", legendDiff="averages_Ads_diff",xmax = 45, ymax = 0.1)

plot.des_blankDiffPlot(analyse.DES_blank1_diff_list, analyse.DES_blank2_diff_list, analyse.DES_blankDiff_list, 'blanks_diffs_des',\
																				'Difference between lines', legendOne="blank1_Des_average", legendTwo="blank2_Des_average", legendDiff="averages_Des_diff",xmax = 45, ymax = 0.1)

# ############################################# Simple plot: Aliq3 #############################################

# # w/o blank subtraction #

# plot.aliqSimplePlot(analyse.ADSaliq3_ads_list, analyse.DESaliq3_des_list, 'aliq3_analysis_raw', 'Adsorption',\
# 										 			'Desorption', xmax = 45, ymax = 20, yAxisLabel = 'delta mass (mg)')

# # w/ blank subtraction #

# plot.aliqSimplePlot(analyse.ADSaliq3_ads_list_BlankCorr, analyse.DESaliq3_des_list_BlankCorr, 'aliq3_analysis_blank_corr', 'Adsorption',\
# 													'Desorption', xmax = 45, ymax = 20, yAxisLabel = 'delta mass (mg)')


# 	# Note: Replace all the prints by the plots. To see run this like: python run.py > check.txt
	
# ######################################### Many plots: blank diffs. #########################################

# 	plot.ads_blankManyPlot([diff['diff'] for diff in analyse.diff_ads_blank], 'many_blank_diffs_ads',\
# 						   													   xmax = 45, ymax = 0.2)
# 	plot.des_blankManyPlot([diff['diff'] for diff in analyse.diff_des_blank], 'many_blank_diffs_des',\
# 						   													   xmax = 45, ymax = 0.2)
	
# ######################################### Diff plot: blanks and their diffs. #########################################

	# index = 0
	# for diff in analyse.diff_ads_blank:
	# 	origin1 = "Blank Line 1: %s" %analyse.origin_blanks[diff['i']]
	# 	origin2 = "Blank Line 2: %s" %analyse.origin_blanks[diff['j']]

	# 	plot.ads_blankDiffPlot(analyse.ads_blank[diff['i']], analyse.ads_blank[diff['j']], diff['diff'], 'blanks_diffs_ads',\
	# 						   index, '%s'%origin1, '%s'%origin2, 'Difference between lines', xmax = 45, ymax = 1.2)
	# 	index += 1

	# index = 0
	# for diff in analyse.diff_des_blank:
	# 	origin1 = "Blank Line 1: %s" %analyse.origin_blanks[diff['i']]
	# 	origin2 = "Blank Line 2: %s" %analyse.origin_blanks[diff['j']]

	# 	plot.des_blankDiffPlot(analyse.des_blank[diff['i']], analyse.des_blank[diff['j']], diff['diff'], 'blanks_diffs_des',\
	# 						   index, '%s'%origin1, '%s'%origin2, 'Difference between lines', xmax = 45, ymax = 1.2)
	# 	index += 1

	# print json.dumps([ {'blank1':analyse.ads_blank[diff['i']], 'blank2':analyse.ads_blank[diff['j']], 'diff':diff['diff']} for diff in analyse.diff_ads_blank])
	# print json.dumps([ {'blank1':analyse.des_blank[diff['i']], 'blank2':analyse.des_blank[diff['j']], 'diff':diff['diff']} for diff in analyse.diff_des_blank])

# ######################################### Simple plot: blanks average diffs #########################################

# 	plot.blankSimplePlot(analyse.average_diff_ads_blank, analyse.average_diff_des_blank, 'blanks_avg_diffs',\
# 														 'Adsorption', 'Desorption', xmax = 45, ymax = 1.2)

# ######################################### Simple plot: blanks average. #########################################

	
# 	plot.blankSimplePlot(analyse.average_ads_blank, analyse.average_des_blank, 'blanks_avg', 'Adsorption', 'Desorption',\
# 													xmax = 45, ymax = 1.2)

# 	# plot.ads_aliqManyPlprint self.average_des_blankot(analyse.ads_aliq, 'many_blank_ads_all')
# 	# plot.des_aliqManyPlot(analyse.des_aliq, 'many_blank_des_all')

# ######################################### Many plots: aliq diffs. #########################################

# 	ads_diffs = []
# 	for diff in analyse.diff_ads_aliq:
# 		ads_diffs.append(diff['diff'])
	
# 	plot.ads_aliqManyPlot(ads_diffs, 'aliq_diffs_ads', xmax = 45, ymax = 1.2)
# 	print "Ads Diff size: %d"%len(ads_diffs)

# 	des_diffs = []
# 	for diff in analyse.diff_des_aliq:
# 		des_diffs.append(diff['diff'])

# 	print "Des Diff size: %d"%len(des_diffs)

# 	plot.des_aliqManyPlot(des_diffs, 'aliq_diffs_des', xmax = 45, ymax = 1.2)

# 	# print json.dumps([ diff['diff'] for diff in analyse.diff_ads_aliq])
# 	# print json.dumps([ diff['diff'] for diff in analyse.diff_des_aliq])
	

# ######################################### Diff plot: aliqs and their diffs. #########################################

# 	index  = 0
# 	for diff in analyse.diff_ads_aliq:
# 		origin1 = "Aliq Line 1: %s" %analyse.origin_aliqs[diff['i']]
# 		origin2 = "Aliq Line 2: %s" %analyse.origin_aliqs[diff['j']]

# 		plot.ads_aliqDiffPlot(analyse.ads_aliq[diff['i']], analyse.ads_aliq[diff['j']], diff['diff'], 'aliqs_diffs_ads',\
# 							  index, '%s'%origin1, '%s'%origin2, 'Difference between lines', xmax = 45, ymax = 20)
# 		index += 1

# 	index  = 0
# 	for diff in analyse.diff_des_aliq:
# 		origin1 = "Aliq Line 1: %s" %analyse.origin_aliqs[diff['i']]
# 		origin2 = "Aliq Line 2: %s" %analyse.origin_aliqs[diff['j']]

# 		plot.des_aliqDiffPlot(analyse.des_aliq[diff['i']], analyse.des_aliq[diff['j']], diff['diff'], 'aliqs_diffs_des',\
# 							  index, '%s'%origin1, '%s'%origin2, 'Difference between lines', xmax = 45, ymax = 20)

# 		index += 1

	# print json.dumps([ {'aliq1':analyse.ads_aliq[diff['i']], 'aliq2':analyse.ads_aliq[diff['j']], 'diff':diff['diff']} for diff in analyse.diff_ads_aliq])
	# print json.dumps([ {'aliq1':analyse.des_aliq[diff['i']], 'aliq2':analyse.des_aliq[diff['j']], 'diff':diff['diff']} for diff in analyse.diff_des_aliq])

# # ######################################### Many plots: aliqs corrected. #########################################

	
# # 	plot.ads_aliqManyPlot(analyse.corrected_ads_aliq, 'aliq_ads_corrected', xmax = 45, ymax = 16)
# # 	plot.des_aliqManyPlot(analyse.corrected_des_aliq, 'aliq_des_corrected', xmin = 0, xmax = 45, ymin = 10, ymax = 16)


# ######################################### Simple plot: aliqs corrected average. #########################################

# 	# plot.aliqSimplePlot(analyse.average_corrected_ads_aliq, analyse.average_corrected_des_aliq, 'aliq_corr_avg', 'Adsorption',\
# 	# 														'Desorption', xmax = 45, ymax = 20)

	

# # 	