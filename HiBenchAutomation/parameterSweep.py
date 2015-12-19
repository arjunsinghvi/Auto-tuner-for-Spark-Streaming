# Before running this, make sure all Hadoop, zookeeper and kafka broker processes are up and running.Also make sure the kafka topics are created.

# Create workload dir if not present
#iterate through all parameters
# 	Initialise with default values
# 	Iterate trhugh all values of a paramter 
#       	Pick the benchmark name from BenchMark file
#               	Increment the RunCounter
#               	Change the workload name 
#               	Change the params: make sure all other are default, and this alone is changed.
#               	Start the gendata.sh in one terminal 
#               	Start run.sh in another terminal
#       	Once over, copy the report folder and Spark log file into the identity directory with the counter name as sub dir name.
#       	Clear Spark log files and kafka log files
#       	Clear cache
#       	Kill the spark-submit jobs, kill run.sh terminal and gendata.sh terminal.

import sys
import os
import fileinput
import re
import time

def replace(fileName, regex, newLine):
        for line in fileinput.input(fileName , inplace = True):
                if str(regex) in line:
                        print newLine
                else:
                        print line[:-1]

def setDefaultParameters():
	paramFileName = "Parameters.conf"
	with open(paramFileName) as f:
	    parameters = f.readlines()
	print("Setting defaults")
	for param in parameters:
		words = param.split("\t")
		newLine = words[0]+ "\t"+ words[1]
		replace("/home/ubuntu/software/HiBench-master/conf/99-user_defined_properties.conf", words[0], newLine)
		
def printFile(filename):
	with open(filename) as f:
        	parameters = f.readlines()
	for param in parameters: 
		print param

def calculateTimeToWait():
	intervalSpan = 0
	totalRound = 0
	with open("/home/ubuntu/software/HiBench-master/conf/01-default-streamingbench.conf", "r") as f:
        	configs = f.readlines()
	for config in configs:
        	if "periodic.intervalSpan" in config:
                	intervalSpan = int(re.findall(r'\d+', config)[0])
                	
        	if "periodic.totalRound" in config:
                	totalRound = int(re.findall(r'\d+', config)[0])
        time = intervalSpan * totalRound
        time = time / 1000
	time = time * 3
	return time
        
def clearCache():
	print "Cache clear"
	os.system("sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'")

def killJobs():
	os.system("jps >> processes.txt")
	with open("processes.txt") as f:
        	processes = f.readlines()
	
	for process in processes:
                if "SparkSubmit" in process:
                        id = re.findall(r'\d+', process)
			#print "Killing "+ str(words[0])
                        os.system("kill -9 "+ id[0])
	os.system("rm -f processes.txt")
		
def clearLogFiles():
	os.system("rm -rf /home/ubuntu/software/kafka_2.10-0.8.1/logs")
	os.system("mkdir /home/ubuntu/software/kafka_2.10-0.8.1/logs")

def pickParams():
	paramFileName = "Parameters.conf"
	with open(paramFileName) as f:
        	parameters = f.readlines()
	for param in parameters:
       		words = param.split("\t")
        	p.append(words[0])

def populateConfiguration(destFolder, workload):
	with open("/home/ubuntu/software/HiBench-master/conf/99-user_defined_properties.conf") as f:
                parameters = f.readlines()
        configuration = ""
        for param in parameters:
                for config in p:
                        if config in param:  
                                #value = re.findall(r'\d+', param)[0]
				value = param.split("\t")[1][:-1]
                                configuration += value + ","
        fileName = destFolder + "/benchlog.txt"
	with open(fileName) as q: 
                sparkConfs = q.readlines()
        for sparkConf in sparkConfs:
                if "latency/batchInterval" in sparkConf:
                        value = re.findall(r'\d+\.\d+', sparkConf)[0]
                        configuration += value
	configuration += "\n"
	fileName = workload + "/ML.csv"
        x = open(fileName , "a")
        x.write(configuration)
	

p =[]
runCounter = 0
os.system("mkdir -p Identity")
os.system("mkdir -p Sample")
os.system("mkdir -p Project")
os.system("mkdir -p Grep")
os.system("mkdir -p Wordcount")
os.system("mkdir -p Distinctcount")
os.system("mkdir -p Statistics")

pickParams()

paramFileName ="Parameters.conf"
with open(paramFileName) as f:
	parameters = f.readlines()

#printFile("Config.conf")

for param in parameters:
	#print "Setting default \n"
	setDefaultParameters()
	#printFile("Config.conf")
	words = param[:-1].split("\t")
	values = words[2].split(",")
	for value in values:
		runCounter = runCounter + 1 
		benchFileName = "BenchName.conf"
		with open(benchFileName) as bf:
        		workloads = bf.readlines()
		for workload in workloads:
			os.system("sh /home/ubuntu/run.sh") 
			#print workload[:-1] + " " + str(runCounter) + " "+ words[0]+" "+ value
			#runCounter =  runCounter + 1
			print workload[:-1] + " " + str(runCounter) + " "+ words[0]+" "+ value
			#print workload[:-1]
			#print workload +" "+ words[0] + " "+ value
			newBenchConf = "hibench.streamingbench.benchname"+ "\t"+ workload[:-1]
			replace("/home/ubuntu/software/HiBench-master/conf/99-user_defined_properties.conf", "hibench.streamingbench.benchname" , newBenchConf)
			newParamConf = words[0] + "\t"+ value
			replace("/home/ubuntu/software/HiBench-master/conf/99-user_defined_properties.conf", words[0], newParamConf)
			#printFile("Config.conf")
			
			#os.system("source /home/ubuntu/run.sh")
			os.system("/home/ubuntu/software/HiBench-master/workloads/streamingbench/spark/bin/run.sh &")
			os.system("/home/ubuntu/software/HiBench-master/workloads/streamingbench/prepare/gendata_arjun.sh &")
			
			
			time.sleep(calculateTimeToWait())
				
			destFolderName = workload[:-1] + "/"+ str(runCounter)
			os.system("mkdir -p "+ destFolderName)
			os.system("cp -r /home/ubuntu/software/HiBench-master/report/streamingbench/spark "+  destFolderName)
			os.system("mv /home/ubuntu/logs/sparkLogFiles "+  destFolderName)
			os.system("mkdir /home/ubuntu/logs/sparkLogFiles")
			os.system("cp /tmp/benchlog.txt "+ destFolderName)
			
			f = open("conf", "w")
			f.write(words[0] + " "+ value)
			f.close()
			os.system("mv conf "+ destFolderName)
			
			print "Done"	
			clearLogFiles()
			clearCache()
			killJobs()	
			time.sleep(0.8)			

			#pickParams()
			populateConfiguration(destFolderName, workload[:-1])
