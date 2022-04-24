# Brain-Heart-Analysis 
# https://github.com/dean456/brain-heart-analysis
# Author: Dean Huang (dean4562007@gmail.com)
# Version: 0.2.1 
# Last update: 2022/4/23
# Instruction:
# 1. Setup: python setup.py install
# 2. Usage: python main.py 
#           [-h] or [--help] help
#           [-e] or [--eeg] EEG mode
#           [-c] or [--ecg] ECG(HRV) mode
#           [-s] or [--samplingrate] Sampling frequency (Hz).
#           [-i] or [--inputcsv] input csv file path (only .csv is recognizable) each column is one channel. The header includs channel names.
#           [-w] or [--inputwfdb] input wfdb format folder and filename (include .dat and .hea and/or .atr)
#           [-o] or [--outfolder] a folder name created for outouting reports

import os
import sys
sys.path.append(os.path.abspath(os.getcwd()))
import getopt
import numpy as np
from dataio import DataIO
import warnings
warnings.filterwarnings("ignore")

def main(argv):
	inputfile = ''
	outputfolder = ''
	delimiter = ','
	mode = ''
	iswfdb = 0
	issinglefile=0
	withheader = 1
	header=[]
	showTimeDomain=False
	showFrequencyDomain=False
	try:
		opts, args = getopt.getopt(argv,"hectfs:i:d:bn:w:o:",["help","eeg","ecg","showTimeDomain","showFrequencyDomain","samplingRate","inputcsv=","csvdelimiter=","csvdelimiterwithspace","csvheader=","inputwfdb=","outputfolder="])
	except getopt.GetoptError:
		print("Usage: python main.py")
		print("[-h] or [--help] help")
		print("[-e] or [--eeg] EEG mode")
		print("[-c] or [--ecg] ECG(HRV) mode")
		print("[-t] or [--showTimeDomain] Show/Print Time Domain deta")
		print("[-f] or [--showFrequencyDomain] Show/Print Frequency Domain deta (Only work in ECG mode)")
		print("[-s] or [--samplingrate] Sampling frequency (Hz).")
		print("[-i] input csv file path (only .csv is recognizable)")
		print("[-d] csv file delimiter")
		print("[-b] csv file delimiter with space")
		print("[-n] csv file without a header and needs to input a list of column names")
		print("[-w] input wfdb format folder and filename (include .dat and .hea and/or .atr)")
		print("[-o] folder for outouted reports")
		sys.exit(2)
		
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print('Usage: python main.py [-e/-c] <EEG/ECG mode> [-t] <showTimeDomain> [-f] <showFrequencyDomain> [-s] <sampling rate(Hz)> [-i] <inputcsvfile> [-w] <inputwfdb> [-o] <outputfolder>')
			sys.exit()
		elif opt in ("-e", "--eeg"):
			mode = 'EEG'
		elif opt in ("-c", "--ecg"):
			mode = 'ECG'
		elif opt in ("-t", "--showTimeDomain"):
			showTimeDomain = True
		elif opt in ("-f", "--showFrequencyDomain"):
			showFrequencyDomain = True
		elif opt in ("-s", "--samplingRate"):
			sampling_rate = float(arg)
		elif opt in ("-i", "--inputcsv"):
			if os.path.isfile(str(arg)):
				inputfile=str(arg)
				issinglefile=1
			else:
				inputfile = [os.path.join(str(arg), f) for f in os.listdir(str(arg)) if os.path.isfile(os.path.join(str(arg), f))]
		elif opt in ("-d", "--csvdelimiter"):
			delimiter = str(arg)
		elif opt in ("-b", "--csvdelimiterwithspace"):
			delimiter = " "
		elif opt in ("-n", "--noheader"):
			withheader = 0
			header = arg.split(',')
		elif opt in ("-w", "--inputwfdb"):
			inputfile = str(arg)
			iswfdb = 1
			withheader = 0
		elif opt in ("-o", "--outputfolder"):
			outputfolder = str(arg)
	
	if iswfdb == 1 or issinglefile==1:	
		raw = DataIO(inputfile,iswfdb,withheader,header=header,pathdelimiter=os.sep,csvdelimiter=delimiter)
		raw.getRawPlot(title=mode,outputfolder=outputfolder)
		if mode == 'EEG':
			raw.EEG(sampling_rate,outputfolder,showTimeDomain)
		elif mode == 'ECG':
			raw.HRV(sampling_rate,outputfolder,showTimeDomain,showFrequencyDomain)
		else:
			print('Unknown analysis mode!')
	else:
		for f in inputfile:
			print('Processing: '+f)
			raw = DataIO(f,iswfdb,withheader,header=header,pathdelimiter=os.sep,csvdelimiter=delimiter)
			raw.getRawPlot(title=mode,outputfolder=outputfolder)
			if mode == 'EEG':
				raw.EEG(sampling_rate,outputfolder,showTimeDomain=showTimeDomain)
			elif mode == 'ECG':
				raw.HRV(sampling_rate,outputfolder,showTimeDomain=showTimeDomain,showFrequencyDomain=showFrequencyDomain)
			else:
				print('Unknown analysis mode!')
	
	'''
	iswfdb=0
	eeg = DataIO("testData\\eeg\\s01_ex01_s01.csv",iswfdb,withheader=1,delimiter=os.sep)
	print(eeg.data)
	sampling_rate_eeg = 200
	eeg.getRawPlot(title='EEG',outputfolder="result")
	ekg = DataIO("testData\\ekg\\100",iswfdb,withheader=0,delimiter="\\") # using MIT wfdb format
	sampling_rate_ekg = 360
	def fxn():
		warnings.warn("deprecated", DeprecationWarning)

	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		fxn()
	'''
if __name__ == "__main__":
	main(sys.argv[1:])

