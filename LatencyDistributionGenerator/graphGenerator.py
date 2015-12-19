import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def plotter(latencies,workload_name):
	fig, ax = plt.subplots()

	index = np.arange(len(latencies))
	xticks = list(range(1,len(latencies)+1))
	'''
	opacity = 0.8

	rects1 = plt.bar(index, latencies, bar_width,
	                 alpha=opacity,
	                 color='g',
	                 edgecolor = 'g')
	'''

	plt.plot(xticks, latencies, 'yo-')
	xlabel = "Number of Different Parameters' Configurations"
	plt.xlabel(xlabel)
	plt.ylabel('Latency (ms)')
	title_label = "Latency Distribution for "+workload_name+" Workload"
	plt.title(title_label)
	#plt.xticks(index, xticks)
	#fig.autofmt_xdate()
	plt.savefig(workload_name+".png", format='png', dpi=1000, bbox_inches='tight')


#latencies = [1,2,3,4,5,4,3,2,1]
#plotter(latencies,"Grep")

base_dir = "./raw_latencies/"
workload_dirs = ["identity"]#,"sample","project","grep","wordcount","distinctcount"]
workload_name = ["Identity","Sample","Project","Grep","Word Count","Distinct Word Count"]

for index in range(0,len(workload_dirs)):
	curFilePath = base_dir+workload_dirs[index]+"/ML.csv"
	fp = open(curFilePath,"r")
	lines = fp.read().split("\n")
	lines = [line for line in lines if line !=""]
	latencies = []
	for line in lines:
		latencies.append(float(line.split(",")[-1]))
	latencies.sort()
	print len(latencies)
	plotter(latencies,workload_name[index])
