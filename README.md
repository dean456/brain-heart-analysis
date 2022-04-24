# Brain-Heart-Analysis
1. Application: Analyse HRV and EEG in a shot 
2. Author: Dean Huang (dean4562007@gmail.com)
3. Version: 0.2.1 
4. Last update: 2022/4/25
5. Quick Start:
6. Instruction:

(1) Setup: python setup.py install

(2) Usage: python main.py
		   [-h] or [--help] help
	     [-e] or [--eeg] EEG mode
		   [-c] or [--ecg] ECG(HRV) mode
		   [-t] or [--showTimeDomain] Show/Print Time Domain deta
		   [-f] or [--showFrequencyDomain] Show/Print Frequency Domain deta (Only work in ECG mode)
		   [-s] or [--samplingrate] Sampling frequency (Hz)
		   [-i] path or folder of the input csv file(s) (only .csv and .txt are recognizable)
		   [-d] delimiter of the csv file(s)
		   [-b] if the csv file delimiter is space (eg. " ")
		   [-n] if csv file without a header, you needs to input a list of column names, eg. "id,C1,C2,C3"
		   [-w] input wfdb format file (include .dat and .hea and/or .atr), eg. "wfdb/100"
		   [-o] the folder for output reports")

6. Example:

(1) a single eeg .csv file with sampling frequency 200 Hz:
python main.py -e -i testData\eeg\s01_ex01_s01.csv -s 200 -o eeg_result_single_file

(2) multiple eeg .csv files in the folder "testData\eeg":
python main.py -e -i testData\eeg -s 200 -o eeg_result_multiple_files

(3) a wfdb formatted ekg file named 100:
python main.py -c -w testData\ekg_wfdb\100 -s 360 -o ekg_result_single_file

(4) a single ekg .txt file named sub01_220217_pre_0100.txt with a header list [id,C1,C2,C3,C4,C5], if you want to see the TimeDomainPlot, add "-t":
python main.py -c -i testData\ekg_csv\sub01_220217_pre_0100.TXT -s 125 -b -n id,C1,C2,C3,C4,C5 -o ekg_result_single_file -t

(5) multiple ekg .txt files in the folder "testData\ekg_csv":
python main.py -c -i testData\ekg_csv -s 125 -b -n ID,L1,L2,L3,L4,L5 -o ekg_result_multiple_files

Enjoy your research!
