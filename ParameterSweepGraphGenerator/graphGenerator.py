import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def plotter(latencies,parameters_name, parameter_value):
	fig, ax = plt.subplots()

	index = np.arange(len(latencies))
	bar_width = 0.35

	opacity = 0.8

	rects1 = plt.bar(index, latencies, bar_width,
	                 alpha=opacity,
	                 color='g',
	                 edgecolor = 'g')

	xlabel = "'"+parameters_name+"' Value"
	plt.xlabel(xlabel)
	plt.ylabel('Latency (ms)')
	ylabel = "Impact of tuning '"+parameters_name+"' on latency"
	plt.title(ylabel)
	plt.xticks(index + bar_width/2.0, parameter_value)
	fig.autofmt_xdate()
	plt.savefig(parameters_name+".png", format='png', dpi=1000, bbox_inches='tight')

fp = open("ParameterSweep.csv","r")
lines = fp.read().split("\r\n")



parameters= [lines[0:4], lines[4:9], lines[9:14], lines[14:19], lines[19:22], lines[22:25], lines[25:28], lines[28:32], lines[32:36]]
for parameter in parameters:
	parameter_name = parameter[0]
	parameter_values = []
	latencies = []
	for row in parameter[1:]:
		information = row.split(",")
		parameter_values.append(information[0])
		latencies.append(float(information[1]))

	plotter(latencies,parameter_name,parameter_values)