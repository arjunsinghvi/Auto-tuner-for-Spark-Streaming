import json
from pprint import pprint
import sys 

'''
Current Features :

1. Total Number of Stages  -- Done
2. Total Number of Tasks   -- Done
3. Total Number of RDDs	   -- Done
4. Average Number of Tasks/Stage -- Done
5. Average Number of RDDs/Stage -- Done
6. Total Number of Wide Dependencies or Shuffle -- Done
7. Average Pipelining Length/Stage   ::::: Isn't this same as (5)
8. Total Number of stateless transformations -- Done
9. Total Number of stateful transformations -- Done
10. Total Number of output operations -- Done
11. Average Number of stateless transformations/Stage -- Done
12. Average Number of stateful transformations/Stage -- Done
13. Average Number of output operations/Stage -- Done
14. Average Stage Dependency Length :::: Should we do this? 

'''

stateless_transformations = ["kafka","map", "flatmap", "filter", "repartition", "union", "count", "reduce", "countbyvalue","reducebykey","join","cogroup","transform"]
stateful_transformations = ["updatestatebykey","window","countbywindow","reducebywindow","reducebykeyandwindow","countbyvalueandwindow"]
output_operations = ["print","saveastextfiles","saveasobjectfiles","saveashadoopfiles","foreachrdd"]

total_task_count = 0
total_rdd_count = 0
total_stages_count = 0
average_task_count = 0
average_rdd_count = 0
wide_dependencies_count = 0
stateless_transformations_count = 0
stateful_transformations_count = 0
output_operations_count = 0

fp = open(sys.argv[1],"r")
#fp = open("wordcount","r")
lines = fp.read().split("\n")
lines = [line for line in lines if line !=""]
job_json_text = ""

for line in lines:
	if line.startswith("{\"Event\":\"SparkListenerJobStart\""):
		job_json_text = line
		break


#Keys for the JSON obj : u'Submission Time' (X),u'Stage IDs',u'Properties'(X),u'Job ID'(X),u'Stage Infos',u'Event'(X)
job_json_object = json.loads(job_json_text)

total_stages_count = len(job_json_object["Stage IDs"])

stages_list = job_json_object["Stage Infos"]


#Keys for each Stage = u'Stage Attempt ID' (X),u'Number of Tasks',u'Parent IDs',u'Stage ID',u'RDD Info',u'Stage Name' (???),u'Details' (X),u'Accumulables' (X)
for stage in stages_list:
	total_task_count += int(stage["Number of Tasks"])
	total_rdd_count += int(len(stage['RDD Info']))
	for rdd in stage['RDD Info']:
#Keys for each RDD = u'RDD ID'(X), u'Parent IDs', u'Name'(X), u'ExternalBlockStore Size'(X), u'Storage Level'(X), u'Disk Size'(X), u'Memory Size'(X), u'Number of Partitions'(X), u'Scope', u'Number of Cached Partitions'(X)
		rdd_scope = eval(str(rdd['Scope']))
		operation = rdd_scope['name'].split('@')[0].split(" ")[0].split("\n")[0].lower()
		#print operation 
		if operation in stateless_transformations:
			stateless_transformations_count +=1
		elif operation in stateful_transformations:
			stateful_transformations_count +=1
		elif operation in output_operations:
			output_operations_count += 1

wide_dependencies_count = total_stages_count - 1
average_rdd_count = (total_rdd_count * 1.0)/total_stages_count
average_task_count = (total_task_count * 1.0)/total_stages_count
average_stateless_count = (stateless_transformations_count*1.0)/total_stages_count
average_stateful_count = (stateful_transformations_count*1.0)/total_stages_count
average_output_count = (output_operations_count*1.0)/total_stages_count

'''
print "Total Stages : "+str(total_stages_count)
print "Total Task Count : "+str(total_task_count)
print "Total RDD Count : "+str(total_rdd_count)
print "Average Task Count : "+str(average_task_count)
print "Average RDD Count : "+str(average_rdd_count)
print "Wide Dependencies Count : "+str(wide_dependencies_count)
print "Total Stateless Operations Count : "+str(stateless_transformations_count)
print "Total Stateful Operations Count : "+str(stateful_transformations_count)
print "Total Output Operations Count : "+str(output_operations_count)
print "Average Stateless Operations Count : "+str(average_stateless_count)
print "Average Stateful Operations Count : "+str(average_stateful_count)
print "Average Output Operations Count : "+str(average_output_count)
'''

feature_names = ["# of stages","# of tasks","# of RDDs","Avg. # of tasks","Avg. # of RDDs","# of wide dependencies","# of stateless operations","# of stateful operations","# of output operations","Avg. # of stateless operations","Avg. # of stateful operations","Avg. # of output operations"]

print str(total_stages_count)+","+str(total_task_count)+","+str(total_rdd_count)+","+str(average_task_count)+","+str(average_rdd_count)+","+str(wide_dependencies_count)+","+str(stateless_transformations_count)+","+str(stateful_transformations_count)+","+str(output_operations_count)+","+str(average_stateless_count)+","+str(average_stateful_count)+","+str(average_output_count)

