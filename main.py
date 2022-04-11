import os
import sys
sys.path.append(os.path.abspath(os.getcwd()))
from dataio import DataIO, MyJsonEncoder
import numpy as np
import csv
import wfdb
from IPython.display import display
import matplotlib 
matplotlib.use('Qt5Agg') # set the 'Qt5Agg' backend to support interactive mode on Windows and macOS
import matplotlib.pyplot as plt
import biosppy
import glob
import pyhrv
import pyhrv.tools as tools
import json 

# DataIO
eeg = DataIO("testData\\eeg\\s01_ex01_s01.csv","csv",withheader=1,delimiter="\\")
sampling_rate_eeg = 125
ekg = DataIO("testData\\ekg\\100","wfdb",withheader=0,delimiter="\\") # using MIT wfdb format
sampling_rate_ekg = 360
time_interval_ekg= 1/sampling_rate_ekg*1000 #ms

#print(eeg.data) #np.array
#print(ekg.data) #np.array
#eeg.getPlot(title='EEG')
#ekg.getPlot(title='EKG')

# Load sample ECG signal & extract R-peaks using BioSppy
signal = ekg.data[:,1] # in mV
signal, rpeaks = biosppy.signals.ecg.ecg(signal, sampling_rate=sampling_rate_ekg, show=False)[1:3] # return ts(second), filtered ECG(mV), rpeaks(location indice)

# Compute NNI
nni = tools.nn_intervals(rpeaks*time_interval_ekg)

# Time Domain Settings
settings_time = {
    'threshold': 50,            # Computation of NNXX/pNNXX with 50 ms threshold -> NN50 & pNN50
    'plot': True,               # If True, plots NNI histogram
    'binsize': 7.8125           # Binsize of the NNI histogram
}

# Frequency Domain Settings
settings_welch = {
    'nfft': 2 ** 12,            # Number of points computed for the FFT result
    'detrend': True,            # If True, detrend NNI series by subtracting the mean NNI
    'window': 'hanning'         # Window function used for PSD estimation
}

settings_lomb = {
    'nfft': 2**8,               # Number of points computed for the Lomb PSD
    'ma_size': 5                # Moving average window size
}

settings_ar = {
    'nfft': 2**12,              # Number of points computed for the AR PSD
    'order': 32                 # AR order
}

# Nonlinear Parameter Settings
settings_nonlinear = {
    'short': [4, 16],           # Interval limits of the short term fluctuations
    'long': [17, 64],           # Interval limits of the long term fluctuations
    'dim': 2,                   # Sample entropy embedding dimension
    'tolerance': None           # Tolerance distance for which the vectors to be considered equal (None sets default values)
}

# Compute the pyHRV parameters
results = pyhrv.hrv(nni=nni,
				sampling_rate=sampling_rate_ekg,
				interval=[0, 10], 
				plot_ecg=True,
				plot_tachogram=True,
				show=False,
				kwargs_time=settings_time,
				kwargs_welch=settings_welch,
				kwargs_ar=settings_ar,
				kwargs_lomb=settings_lomb,
				kwargs_nonlinear=settings_nonlinear)
#fbands=None
#If fbands is none, the default values for the frequency bands will be set.
#VLF: [0.00Hz - 0.04Hz]
#LF: [0.04Hz - 0.15Hz]
#HF: [0.15Hz - 0.40Hz]				

#print(results.as_dict())

resultfolder ="results\\"
reportname='hrv_results'
if not os.path.isdir(resultfolder):
	os.mkdir(resultfolder)

pyhrv.tools.hrv_export(results, path=resultfolder, efile=reportname, comment=None, plots=True)
		
#pyhrv.tools.hrv_report(results, path=resultfolder, rfile=reportname, nni=nni, info={'file':ekg.filename,'fs':sampling_rate_ekg}, file_format='txt', delimiter=',', hide=False, plots=True)


		

