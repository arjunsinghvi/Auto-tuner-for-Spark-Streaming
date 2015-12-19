#read the csv, put the last element of each line into a list
#sort the array
#find out the 33rd, 67 percentile
#read the csv, replace the last column with l,m,h
import numpy as np
import csv
import fileinput


final_filename="crossvalidation_dataset.csv"
baseDir = "./raw_latencies/"
workloads = ["identity","project","sample","grep","wordcount","distinctcount"]
workload_features = ["1,1,2,1.0,2.0,0,2,0,0,2.0,0.0,0.0,","1,1,3,1.0,3.0,0,2,0,1,2.0,0.0,1.0,","1,2,3,2.0,3.0,0,3,0,0,3.0,0.0,0.0,","1,1,3,1.0,3.0,0,3,0,0,3.0,0.0,0.0,","2,13,5,6.5,2.5,1,5,0,0,2.5,0.0,0.0,","2,13,5,6.5,2.5,1,5,0,0,2.5,0.0,0.0,"]

for index in range(len(workloads)):
	sample_file = baseDir+workloads[index]+"/ML.csv"
	bucket_filename = workloads[index]+".csv"
	my_list=[]
	#read the file to calculate the percentiles
	print workloads[index]
	with open(sample_file, 'rb') as f:
	    mycsv=csv.reader(f)
	    for row in mycsv:
	        latency = row[len(row)-1]
		#print latency
		#print "hello"
		my_list.append(latency)
	f.close()

	#convert the list into a numpy array
	a = np.array(my_list,dtype=float)

	#calculate the 33rd and 67th percentile
	percentile_33 = float(np.percentile(a, 33)) # return 33rd percentile
	percentile_67 = float(np.percentile(a, 67)) # return 67th percentile
	percentile_50 = float(np.percentile(a, 50)) # return 50th percentile
	percentile_10 = float(np.percentile(a, 10)) # return 10th percentile
	percentile_90 = float(np.percentile(a, 90)) # return 90th percentile
	percentile_20 = float(np.percentile(a, 20)) # return 20th percentile
	percentile_80 = float(np.percentile(a, 80)) # return 80th percentile

	#print "percentile 33,67,50,10,90,20,80 :",percentile_33,percentile_67,percentile_50,percentile_10,percentile_90,percentile_20,percentile_80

	final_file = open(final_filename,'a')
	bucket_file = open(bucket_filename,'a')

	#read the file again to replace the latency with buckets
	with open(sample_file, 'rb') as f:
	    mycsv2=csv.reader(f)
	    for row in mycsv2:
	        latency = float(row[len(row)-1])
		if latency < percentile_33:
			bucket='0'
		elif latency < percentile_67:
			bucket='1'
		else: 
			bucket='2'
		row_string=','.join(row)
		newrow = ','.join(row[:-1])+ "," + bucket +"\n"
		newrow = workload_features[index]+newrow
		#print newrow
		newrow = newrow.replace("g,",",")
		newrow = newrow.replace("false","0")
		newrow = newrow.replace("true","1")
		newrow = newrow.replace("hash","0")
		newrow = newrow.replace("tungsten-sort","2")
		newrow = newrow.replace("sort","1")
		#print newrow
		final_file.write(newrow)
		bucket_file.write(newrow)
   	