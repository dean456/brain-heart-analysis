import os
import numpy as np
import csv
import wfdb
from IPython.display import display
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json

class DataIO:
	def __init__(self,datapath,datatype,withheader=1,delimiter="/"):
		pathname, extension=os.path.splitext(datapath)
		pathsplit=pathname.split(delimiter)
		self.datapath=datapath
		self.datatype=datatype
		self.pathname=pathname
		self.filename=pathsplit[-1]
		self.withheader=withheader
		self.header=[]
		self.data=[]
		if (datatype=='csv'):
			self.data=self.getCSVdata()
		elif(datatype=='wfdb'):
			self.data=self.getWFDBdata()
		else:
			print('non-support dataformat')
	
	def getCSVdata(self):
		with open(self.datapath, newline='') as csvfile:
			rows = csv.reader(csvfile, delimiter=',')
			data=[]
			isheader = 0
			if (self.withheader==1):
				isheader = 1
			for row in rows:
				if (isheader == 1):
					self.header = row
					isheader = 0
				else:
					data.append(row)
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
				
	def getPlot(self,title='Waveforms',legend='data',labelx='T(s)',labely='Amplitude(mV)',imagefolder='images', color='k-', channels='all'):
		if (self.datatype=='csv'):
			if not os.path.isdir(imagefolder):
				os.mkdir(imagefolder)
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
				else:
					plt.legend([legend],loc="best",prop=font)
				plt.title(title)
				plt.xlabel(labelx)
				plt.ylabel(labely)
				plt.grid()
				#plt.show()
				plt.savefig(imagefolder+"/"+self.filename+"_ch"+str(ch)+".png") # default png
				plt.close()
			return print("Complete csv plots, please check the image folder")
		elif (self.datatype=='wfdb'):
			#signals, fields = wfdb.rdsamp(self.datapath)
			#wfdb.plot_items(signal=signals, fs=fields['fs'], title=title)
			np.savetxt(self.pathname+".csv", self.data, fmt='%f', delimiter=',', newline='\n',header=','.join(map(str, self.header))) # fm='%1.4f'
			newCSV=DataIO(self.filename+".csv","csv",withheader=1)
			newCSV.getPlot(title=title)
			return print("Complete wfdb as the above csv plot")
		else: 
			return print("Not a recognizable format")
			
class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyJsonEncoder, self).default(obj)

#Usage: with open("hrv_result.json", "w+") as outfile:
	#json.dump(results.as_dict(), outfile)
	#json.dump(results.as_dict(), outfile, cls=MyJsonEncoder)
#with open(resultfolder+"\hrv_result.txt", 'w+') as f: 
#    for key, value in results.as_dict().items(): 
#        f.write('%s:%s\n' % (key, value))
#with open('hrv_result.txt','w') as data: 
#      data.write(str(results.as_dict()))	