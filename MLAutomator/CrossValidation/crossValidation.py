import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import cross_val_predict
from sklearn.tree import export_graphviz
from sklearn.metrics import confusion_matrix
import sys
import os
from random import shuffle

'''
Format of csv 
1st row has the headers
Last column contains the class which is 0,1,2

How to run the program:
python multipleModels.py <filename of the csv containing data> <destination folder name which will be created>
'''

os.system("mkdir "+sys.argv[2])
curDir_path = "./"+sys.argv[2]+"/"

def plotter(accuracies,stdeviation,models):
	fig, ax = plt.subplots()

	index = np.arange(len(models))
	bar_width = 0.35

	opacity = 0.8
	error_config = {'ecolor': '0.3'}

	rects1 = plt.bar(index, accuracies, bar_width,
	                 alpha=opacity,
	                 color='g',
	                 edgecolor = 'g',
	                 yerr=stdeviation,
	                 error_kw=error_config)

	plt.xlabel('Learning Algorithm')
	plt.ylabel('Mean Accuracy (%)')
	plt.title("Mean Accuracy vs Machine Learning Algorithm")
	plt.xticks(index + bar_width/2.0, models)
	fig.autofmt_xdate()
	plt.savefig(curDir_path+'accuracies.png', format='png', dpi=1000, bbox_inches='tight')

def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(3)
    plt.xticks(tick_marks, ["Low\nLatency","Medium\nLatency","High\nLatency"],)
    plt.yticks(tick_marks, ["Low\nLatency","Medium\nLatency","High\nLatency"])
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def generate_confusion_matrix(y_test, y_pred, model_name):

	cm = confusion_matrix(y_test, y_pred, labels = [0.0,1.0,2.0])
	title_name = 'Confusion Matrix for '+model_name
	file_name = curDir_path+model_name+".png"
	cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
	plt.figure()
	plot_confusion_matrix(cm_normalized, title=title_name)
	plt.savefig(file_name, format='png', dpi=1000, bbox_inches='tight')

#Accuracy and Std Deviation
accuracy = []
stdeviation = []
models = ["AdaBoost", "Random Forest", "Naive Bayes", "Naive Bayes (Bagging)","Decision Tree","Decision Tree (Bagging)","Linear SVM","Linear SVM (Bagging)","Non-linear SVM","Non-linear SVM(Bagging)"]

#Read the dataset
data_reader = csv.reader(open(sys.argv[1], "rb"))
data_reader.next()

data = []
for row in data_reader:
	data.append([float(x) for x in row])

data = np.array(data)

shuffle(data)

input_data = data[0:len(data),:-1]
output_data = data[0:len(data),-1]

#Now test on different models to generate accuracies and std deviation
model = AdaBoostClassifier(n_estimators=100)
accuracies = cross_val_score(model,input_data,output_data,'accuracy',10)
print "Boosting : "+","+str(accuracies.min()*100.0)+","+str(accuracies.mean()*100.0)+","+str(accuracies.max()*100.0)
metrics_pair = ("%0.2f,%0.2f" % (accuracies.mean() * 100.0 , accuracies.std() * 100.0))
accuracy.append(float(metrics_pair.split(",")[0]))
stdeviation.append(float(metrics_pair.split(",")[1]))
y_pred = cross_val_predict(model,input_data,output_data,10)
generate_confusion_matrix(output_data,y_pred,models[0])

model = RandomForestClassifier(n_estimators = 100)
accuracies = cross_val_score(model,input_data,output_data,'accuracy',10)
print "RFs : "+","+str(accuracies.min()*100.0)+","+str(accuracies.mean()*100.0)+","+str(accuracies.max()*100.0)
metrics_pair = ("%0.2f,%0.2f" % (accuracies.mean() * 100.0 , accuracies.std() * 100.0))
accuracy.append(float(metrics_pair.split(",")[0]))
stdeviation.append(float(metrics_pair.split(",")[1]))
y_pred = cross_val_predict(model,input_data,output_data,10)
generate_confusion_matrix(output_data,y_pred,models[1])


model = MultinomialNB()
accuracies = cross_val_score(model,input_data,output_data,'accuracy',10)
print "MultinomialNB : "+","+str(accuracies.min()*100.0)+","+str(accuracies.mean()*100.0)+","+str(accuracies.max()*100.0)
metrics_pair = ("%0.2f,%0.2f" % (accuracies.mean() * 100.0 , accuracies.std() * 100.0))
accuracy.append(float(metrics_pair.split(",")[0]))
stdeviation.append(float(metrics_pair.split(",")[1]))
y_pred = cross_val_predict(model,input_data,output_data,10)
generate_confusion_matrix(output_data,y_pred,models[2])

model = BaggingClassifier(model,max_samples=1.0, max_features=1.0)
accuracies = cross_val_score(model,input_data,output_data,'accuracy',10)
print "Bagging MultinomialNB : "+","+str(accuracies.min()*100.0)+","+str(accuracies.mean()*100.0)+","+str(accuracies.max()*100.0)
metrics_pair = ("%0.2f,%0.2f" % (accuracies.mean() * 100.0 , accuracies.std() * 100.0))
accuracy.append(float(metrics_pair.split(",")[0]))
stdeviation.append(float(metrics_pair.split(",")[1]))
y_pred = cross_val_predict(model,input_data,output_data,10)
generate_confusion_matrix(output_data,y_pred,models[3])

model = DecisionTreeClassifier()
accuracies = cross_val_score(model,input_data,output_data,'accuracy',10)
print "DecisionTree : "+","+str(accuracies.min()*100.0)+","+str(accuracies.mean()*100.0)+","+str(accuracies.max()*100.0)
metrics_pair = ("%0.2f,%0.2f" % (accuracies.mean() * 100.0 , accuracies.std() * 100.0))
accuracy.append(float(metrics_pair.split(",")[0]))
stdeviation.append(float(metrics_pair.split(",")[1]))
y_pred = cross_val_predict(model,input_data,output_data,10)
generate_confusion_matrix(output_data,y_pred,models[4])

model = BaggingClassifier(model,max_samples=1.0, max_features=1.0)
accuracies = cross_val_score(model,input_data,output_data,'accuracy',10)
print "Bagging DTs : "+","+str(accuracies.min()*100.0)+","+str(accuracies.mean()*100.0)+","+str(accuracies.max()*100.0)
metrics_pair = ("%0.2f,%0.2f" % (accuracies.mean() * 100.0 , accuracies.std() * 100.0))
accuracy.append(float(metrics_pair.split(",")[0]))
stdeviation.append(float(metrics_pair.split(",")[1]))
y_pred = cross_val_predict(model,input_data,output_data,10)
generate_confusion_matrix(output_data,y_pred,models[5])

model = LinearSVC()
accuracies = cross_val_score(model,input_data,output_data,'accuracy',10)
print "LinearSVC : "+","+str(accuracies.min()*100.0)+","+str(accuracies.mean()*100.0)+","+str(accuracies.max()*100.0)
metrics_pair = ("%0.2f,%0.2f" % (accuracies.mean() * 100.0 , accuracies.std() * 100.0))
accuracy.append(float(metrics_pair.split(",")[0]))
stdeviation.append(float(metrics_pair.split(",")[1]))
y_pred = cross_val_predict(model,input_data,output_data,10)
generate_confusion_matrix(output_data,y_pred,models[6])

model = BaggingClassifier(model,max_samples=1.0, max_features=1.0)
accuracies = cross_val_score(model,input_data,output_data,'accuracy',10)
print "Bagging LinearSVCs : "+","+str(accuracies.min()*100.0)+","+str(accuracies.mean()*100.0)+","+str(accuracies.max()*100.0)
metrics_pair = ("%0.2f,%0.2f" % (accuracies.mean() * 100.0 , accuracies.std() * 100.0))
accuracy.append(float(metrics_pair.split(",")[0]))
stdeviation.append(float(metrics_pair.split(",")[1]))
y_pred = cross_val_predict(model,input_data,output_data,10)
generate_confusion_matrix(output_data,y_pred,models[7])

model = SVC()
accuracies = cross_val_score(model,input_data,output_data,'accuracy',10)
print "NonLinear SVC : "+","+str(accuracies.min()*100.0)+","+str(accuracies.mean()*100.0)+","+str(accuracies.max()*100.0)
metrics_pair = ("%0.2f,%0.2f" % (accuracies.mean() * 100.0 , accuracies.std() * 100.0))
accuracy.append(float(metrics_pair.split(",")[0]))
stdeviation.append(float(metrics_pair.split(",")[1]))
y_pred = cross_val_predict(model,input_data,output_data,10)
generate_confusion_matrix(output_data,y_pred,models[8])

model = BaggingClassifier(model,max_samples=1.0, max_features=1.0)
accuracies = cross_val_score(model,input_data,output_data,'accuracy',10)
print "Bagging NonLinearSVCs : "+","+str(accuracies.min()*100.0)+","+str(accuracies.mean()*100.0)+","+str(accuracies.max()*100.0)
metrics_pair = ("%0.2f,%0.2f" % (accuracies.mean() * 100.0 , accuracies.std() * 100.0))
accuracy.append(float(metrics_pair.split(",")[0]))
stdeviation.append(float(metrics_pair.split(",")[1]))
y_pred = cross_val_predict(model,input_data,output_data,10)
generate_confusion_matrix(output_data,y_pred,models[9])

plotter(accuracy,stdeviation,models)

