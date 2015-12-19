import os 
import sys 
import pickle 
import fileinput
import re
import time
import itertools

def replace(fileName, regex, newLine):
        for line in fileinput.input(fileName , inplace = True):
                if str(regex) in line:
                        print newLine
                else:
                        print line[:-1]

def applyConfig(param):
	for key, val in param.iteritems(): 
		newLine = key +"\t"+ val
		replace("/home/ubuntu/software/HiBench-master/conf/99-user_defined_properties.conf", key, newLine)	


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

def populateConfiguration(destFolder, workload):
        with open("/home/ubuntu/software/HiBench-master/conf/99-user_defined_properties.conf") as f:
                parameters = f.readlines()
        configuration = ""
        for param in parameters:
                for config in p:
                        if config in param:
                                #value = re.findall(r'\d+', param)[0]
                                #configuration += value + ","
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

def pickParams(param):
	for x in param: 
		p.append(x)
	

def generateParams():
	fp = open("Parameters.conf","r")
	lines = fp.read().split("\n")
	lines = [line.split(" ") for line in lines if line!=""]
	
	parameter_mapping = {}

	parameter_names = []
	parameter_values = []
	for line in lines:
		parameter_names.append(line[0])
		parameter_values.append(line[2].split(","))

	parameter_combinations = list(itertools.product(*parameter_values))

	for combination in parameter_combinations:
		temp_dict = {}
		for index in range(0,len(combination)):
			temp_dict[parameter_names[index]] = combination[index]
		Parameters.append(temp_dict)

p =[]
runCounter = 0
os.system("mkdir -p Identity")
os.system("mkdir -p Sample")
os.system("mkdir -p Project")
os.system("mkdir -p Grep")
os.system("mkdir -p Wordcount")
os.system("mkdir -p Distinctcount")

Parameters = []
generateParams()
pickParams(Parameters[0])

for param in Parameters: 
	applyConfig(param)
	runCounter = runCounter + 1
	benchFileName = "BenchName.conf"
	with open(benchFileName) as bf:
        	workloads = bf.readlines()
        for workload in workloads:
        	os.system("sh /home/ubuntu/run.sh")

                newBenchConf = "hibench.streamingbench.benchname"+ "\t"+ workload[:-1]
                replace("/home/ubuntu/software/HiBench-master/conf/99-user_defined_properties.conf", "hibench.streamingbench.benchname" , newBenchConf)
               	os.system("/home/ubuntu/software/HiBench-master/workloads/streamingbench/spark/bin/run.sh &")
	        os.system("/home/ubuntu/software/HiBench-master/workloads/streamingbench/prepare/gendata_arjun.sh &")

                time.sleep(calculateTimeToWait())

                destFolderName = workload[:-1] + "/"+ str(runCounter)
		
                os.system("mkdir -p "+ destFolderName)
                #os.system("cp -r /home/ubuntu/software/HiBench-master/report/streamingbench/spark "+  destFolderName)
                #os.system("mv /home/ubuntu/logs/sparkLogFiles "+  destFolderName)
                #os.system("mkdir /home/ubuntu/logs/sparkLogFiles")
                os.system("cp /tmp/benchlog.txt "+ destFolderName)

		f = open("conf", "w")
                f.write(str(param))
                f.close()
                os.system("mv conf "+ destFolderName)

                print "Done"
                clearLogFiles()
                clearCache()
                killJobs()
                time.sleep(0.8)

                #pickParams()
                populateConfiguration(destFolderName, workload[:-1])


		
