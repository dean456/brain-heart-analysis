import os
import numpy as np
import csv
import wfdb
from IPython.display import display
import matplotlib 
matplotlib.use('Qt5Agg') # set the 'Qt5Agg' backend to support interactive mode on Windows and macOS
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json
import biosppy
import glob
import pyhrv
import pyhrv.tools as tools


class DataIO:
	def __init__(self,datapath,iswfdb,withheader=1,header=[],pathdelimiter=os.sep,csvdelimiter=','):
		pathname, extension=os.path.splitext(datapath)
		pathsplit=pathname.split(pathdelimiter)
		self.datapath=datapath
		self.datatype=extension
		self.pathname=pathname
		self.filename=pathsplit[-1]
		self.withheader=withheader
		self.header=header
		self.data=[]
		if iswfdb == 1:
			self.data=self.getWFDBdata()
			self.datatype='wfdb'
		elif (self.datatype=='.csv'):
			self.data=self.getCSVdata(csvdelimiter)
		elif (self.datatype=='.txt' or self.datatype=='.TXT'):
			self.datatype='.csv'
			self.data=self.getCSVdata(csvdelimiter)
		else:
			print('Unrecognizable dataformat')
	
	def getCSVdata(self,delimiter=','):
		with open(self.datapath, newline='') as csvfile:
			rows = csv.reader(csvfile, delimiter=delimiter)
			data=[]
			isheader = 0
			c_num = len(self.header)
			if (self.withheader==1):
				isheader = 1
			for row in rows:
				if (isheader == 1):
					self.header = row
					isheader = 0
					c_num = len(row)
				else:
					list_tmp = []
					for s in row:
						if not s:
							list_tmp.append(0.0)
						else:
							list_tmp.append(float(s))
					if len(list_tmp) == c_num:
						data.append(list_tmp)
		return np.array(data,dtype=np.float32)
	
	def getWFDBdata(self):
		signals, fields = wfdb.rdsamp(self.datapath)
		samplingFrequency= fields['fs']
		timeinterval=1/samplingFrequency # unit: second
		sampleNum = 0 
		data=[]
		if fields['sig_name']:
			self.header = fields['sig_name']
			self.header.insert(0,'timestamp')
		for row in signals:
			timestamp = timeinterval*sampleNum
			data.append(np.insert(row,0,timestamp))
			sampleNum += 1
		return np.array(data)
		
	def getWFDBheader(self):
		if (self.datatype=='wfdb'):
			signals, fields = wfdb.rdsamp(self.datapath)
			return display((signals, fields))
		else: 
			return print("Not WFDB format")
				
	def getRawPlot(self,title='Waveforms',legend="data",labelx='T(s)',labely='Amplitude(mV)',outputfolder='ecg_waveform_plots', color='k-', channels='all'):
		if (self.datatype=='.csv'):
			s_num = self.data.shape[0]
			if (channels=="all"):
				ch_num = self.data.shape[1]
				channels = range(1,ch_num)
			for ch in channels:
				plt.figure(ch)
				plt.plot(self.data[:,0],self.data[:,ch],color)
				font = fm.FontProperties(family='sans-serif',
										weight='normal',style='normal', size=12)
				if (self.withheader==1):
					plt.legend([self.header[ch]],loc="best",prop=font)
					#plt.legend(['Cz'],loc="best",prop=font)
				elif legend is not None:
					plt.legend([legend],loc="best",prop=font)
				plt.title(title)
				plt.xlabel(labelx)
				plt.ylabel(labely)
				plt.grid()
				#plt.show()
				if not os.path.isdir(outputfolder):
					os.mkdir(outputfolder)
				plt.savefig(outputfolder+"/"+self.filename+"_ch"+str(ch)+".png") # default png
				plt.close()
			return print("Complete csv plots, please check the output folder")
		elif (self.datatype=='wfdb'):
			#signals, fields = wfdb.rdsamp(self.datapath)
			#wfdb.plot_items(signal=signals, fs=fields['fs'], title=title)
			np.savetxt(self.pathname+".csv", self.data, fmt='%f', delimiter=',', newline='\n',header=','.join(map(str, self.header))) # fm='%1.4f'
			newCSV=DataIO(self.pathname+".csv",0,withheader=1)
			newCSV.getRawPlot(title=title,outputfolder=outputfolder)
			return print("Complete wfdb as the above csv plot")
		else: 
			return print("Not a recognizable format")
	
	def getPlot(x=None,y=None,title=None,legend=None,labelx='T(s)',labely='Power',outputfolder='waveform_plots',filename='waveforms',color='b-'):
		if x is not None and y is not None:
			ch_num = y.shape[0]
			if legend is not None:
				l_num = len(legend)
				if (l_num != ch_num):
					return print("inconsistent length of legend")
			fig, axs = plt.subplots(ch_num,sharex=True)
			if title is not None:
				fig.suptitle(title, fontsize=12)
			for ch in range(0,ch_num):
				x_num = x[ch,:].shape[0]
				y_num = y[ch,:].shape[0]
				if (x_num != y_num):
					return print("inconsistent length of inputs")
				if legend is not None:
					axs[ch].plot(x[ch,:],y[ch,:],color,label=legend[ch])
					axs[ch].legend(loc="right")
				else:
					axs[ch].plot(x[ch,:],y[ch,:],color)
			for ax in axs.flat:
				ax.set(xlabel=labelx, ylabel=labely)
			
			#plt.show()
			if not os.path.isdir(outputfolder):
				os.mkdir(outputfolder)
			plt.savefig(outputfolder+os.sep+filename+".png") # default png
			plt.close()
		else:
			return print("missing input data")
	
	def writeCSVdata(data=None,header=None,filename='default',outputfolder='csv_result',delimiter=','):
		if data is not None or header is not None:
			if not os.path.isdir(outputfolder):
				os.mkdir(outputfolder)
			with open(outputfolder+"\\"+filename+".csv", 'w+',newline='') as f: 
				csvwriter=csv.writer(f,delimiter=delimiter)
				for l in range(0,data.shape[1]): 
					if l ==  0:
						csvwriter.writerow(header)
					else:
						csvwriter.writerow(data[:,l-1])
		else:
			return print("Missing data or header for output")
	
	#EEG	
	def EEG(self,sampling_rate_eeg,outputfolder,showTimeDomain=False):
		ch_num = self.data.shape[1]-1
		ch_s= np.s_[1:ch_num+1] # slices
		ch_list = self.header[ch_s] # 0 = timestamp
		print("Input EEG channels:")
		print(ch_list)
		
		fband_header = ['timestamp','theta(4-8Hz)', 'alpha_low(8-10Hz)', 'alpha_high(10-13Hz)', 'beta(13-25Hz)', 'gamma(25-40Hz)']
		fband_num = len(fband_header)
		print("Output Band Power Channels:")
		print(fband_header[1:])
		

		#Extract relevant signal features using default parameters
		ts, eeg_signal, features_ts, theta, alpha_low, alpha_high, beta, gamma, phase_lock_pairs, phase_lock = biosppy.signals.eeg.eeg(signal=self.data[:,ch_s], sampling_rate=sampling_rate_eeg, labels=ch_list, show=showTimeDomain) 
		#Signal_ts(second) Filtered BVP signal, features_ts(second),theta(4-8Hz), alpha_low(8-10Hz), alpha_high(10-13Hz),beta(13-25Hz), gamma(25-40Hz)
		#theta[sample,ch]

		s_num = len(features_ts)
		eeg_rawdata = np.zeros((ch_num,fband_num,s_num))
		for ch in range(0,ch_num):
			eeg_rawdata[ch] = np.c_[np.reshape([features_ts, theta[:,ch], alpha_low[:,ch], alpha_high[:,ch], beta[:,ch], gamma[:,ch]],(fband_num,s_num))]
			DataIO.writeCSVdata(data=eeg_rawdata[ch],header=fband_header,filename=self.filename+"_"+self.header[ch+1]+"_raw_avgpower",outputfolder =outputfolder,delimiter=',')
		
		print("Overlap setting: window size=0.25(s), overlap=0.5")
		#Extract band power features from EEG signals.
		ts, theta, alpha_low, alpha_high, beta, gamma = biosppy.signals.eeg.get_power_features(signal=self.data[:,ch_s], sampling_rate=sampling_rate_eeg, size=0.25, overlap=0.5) # size: window size(seconds), overlap: window overlap ratio (0-1)
		
		s_num = len(features_ts)
		eeg_powdata = np.zeros((ch_num,fband_num,s_num))
		for ch in range(0,ch_num):
			eeg_powdata[ch] = np.c_[np.reshape([features_ts, theta[:,ch], alpha_low[:,ch], alpha_high[:,ch], beta[:,ch], gamma[:,ch]],(fband_num,s_num))]
			DataIO.writeCSVdata(data=eeg_powdata[ch],header=fband_header,filename=self.filename+"_"+self.header[ch+1]+"_overlap_avgpower",outputfolder=outputfolder,delimiter=',')

		# Plot
		fb_s= np.s_[1:fband_num]
		for fb in range(1,fband_num):
			DataIO.getPlot(x=eeg_rawdata[:,0,:],y=eeg_rawdata[:,fb,:],title="EEG Summary "+fband_header[fb],legend=ch_list,outputfolder=outputfolder,filename=self.filename+'_'+fband_header[fb])
			DataIO.getPlot(x=eeg_powdata[:,0,:],y=eeg_powdata[:,fb,:],title="EEG Summary (overlap) "+fband_header[fb],legend=ch_list,outputfolder=outputfolder,filename=self.filename+'_'+fband_header[fb]+'_overlap')

	# ECG
	def HRV(self,sampling_rate_ekg,outputfolder,showTimeDomain=False,showFrequencyDomain=False):	
		ch_num = self.data.shape[1]
		for ch in range(1,ch_num):
			# Load sample ECG signal & extract R-peaks using BioSppy
			print("Load Channel "+str(ch)+"...")
			signal = self.data[:,ch] # in mV
			signal, rpeaks = biosppy.signals.ecg.ecg(signal, sampling_rate=sampling_rate_ekg, show=showTimeDomain)[1:3] # return ts(second), filtered ECG(mV), rpeaks(location indice)

			# Compute NNI
			print("Compute nni...")
			time_interval_ekg= 1/sampling_rate_ekg*1000 #ms
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
			print("Compute HRV frequency domain...")
			results = pyhrv.hrv(nni=nni,
							sampling_rate=sampling_rate_ekg,
							interval=[0, 10], 
							plot_ecg=True,
							plot_tachogram=True,
							show=showFrequencyDomain,
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

			if not os.path.isdir(outputfolder):
				os.mkdir(outputfolder)

			pyhrv.tools.hrv_export(results, path=outputfolder+os.sep, efile=self.filename+"_ch"+str(ch)+"_hrv", comment=None, plots=True)
			print("Complete output!")
				
			#pyhrv.tools.hrv_report(results, path=resultfolder, rfile=reportname, nni=nni, info={'file':ekg.filename,'fs':sampling_rate_ekg}, file_format='txt', delimiter=',', hide=False, plots=True)


#class MyJsonEncoder(json.JSONEncoder):
#    def default(self, obj):
#        if isinstance(obj, np.integer):
#            return int(obj)
#        elif isinstance(obj, np.floating):
#            return float(obj)
#        elif isinstance(obj, np.ndarray):
#            return obj.tolist()
#        else:
#            return super(MyJsonEncoder, self).default(obj)
#Usage: with open("hrv_result.json", "w+") as outfile:
	#json.dump(results.as_dict(), outfile)
	#json.dump(results.as_dict(), outfile, cls=MyJsonEncoder)
#with open(resultfolder+"\hrv_result.txt", 'w+') as f: 
#    for key, value in results.as_dict().items(): 
#        f.write('%s:%s\n' % (key, value))
#with open('hrv_result.txt','w') as data: 
#      data.write(str(results.as_dict()))	