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
import random
'''
Format of csv
1st row has the headers
Last column contains the class which is 0,1,2

How to run the program:
python multipleModels.py <combination one or two> <trial_number>
'''

accuracies = []


def plotter(accuracies,models):
	fig, ax = plt.subplots()

	index = np.arange(len(models))
	bar_width = 0.35

	opacity = 0.8

	rects1 = plt.bar(index, accuracies, bar_width,
	                 alpha=opacity,
	                 color='g',
	                 edgecolor = 'g')

	plt.xlabel('Learning Algorithm')
	plt.ylabel('Testing Accuracy (%)')
	plt.title("Testing Accuracy vs Machine Learning Algorithm")
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


models = ["AdaBoost", "Random Forest", "Naive Bayes", "Naive Bayes (Bagging)","Decision Tree","Decision Tree (Bagging)","Linear SVM","Linear SVM (Bagging)","Non-linear SVM","Non-linear SVM(Bagging)"]
choice = int(sys.argv[1])

if (choice == 1):
	train_files = ['initial_results/distinctcount/ML.csv','initial_results/identity/ML.csv','initial_results/sample/ML.csv','initial_results/grep/ML.csv']
	test_files = ['initial_results/wordcount/ML.csv','initial_results/project/ML.csv']
	base_dir = "./wc_project/"
else:
	train_files = ['initial_results/wordcount/ML.csv','initial_results/identity/ML.csv','initial_results/sample/ML.csv','initial_results/project/ML.csv']
	test_files = ['initial_results/grep/ML.csv','initial_results/distinctcount/ML.csv']
	base_dir = "./dc_grep/"

curDir_path = base_dir+sys.argv[2]+"/"
print base_dir
os.system("mkdir "+base_dir)
print curDir_path
os.system("mkdir "+curDir_path)

training_data = []
testing_data = []

for train_file in train_files:
        train_reader = csv.reader(open((train_file),"rb"))
        for row in train_reader:
                training_data.append([float(x) for x in row])

for test_file in test_files:
        test_reader = csv.reader(open((test_file),"rb"))
        for row in test_reader:
                testing_data.append([float(x) for x in row])


training_data = np.array(training_data)
random.shuffle(training_data)
testing_data = np.array(testing_data)

training_data_input = training_data[0:len(training_data),:-1]
training_data_output = training_data[0:len(training_data),-1]

testing_data_input = testing_data[0:len(testing_data),:-1]
testing_data_output = testing_data[0:len(testing_data),-1]

AdaBoostmodel = AdaBoostClassifier(n_estimators=100) 
AdaBoostmodel.fit(training_data_input,training_data_output)
AdaBoostaccuracy = AdaBoostmodel.score(testing_data_input,testing_data_output)
predicted_output = AdaBoostmodel.predict(testing_data_input)
print "AdaBoost :"+str(AdaBoostaccuracy*100.0)
generate_confusion_matrix(testing_data_output,predicted_output,models[0])
accuracies.append(AdaBoostaccuracy * 100.0)

RFmodel = RandomForestClassifier(n_estimators = 100)
RFmodel.fit(training_data_input,training_data_output)
RFaccuracy = RFmodel.score(testing_data_input,testing_data_output)
predicted_output = RFmodel.predict(testing_data_input)
print "RFs :"+str(RFaccuracy*100.0)
generate_confusion_matrix(testing_data_output,predicted_output,models[1])
accuracies.append(RFaccuracy * 100.0)

NBmodel = MultinomialNB()
NBmodel.fit(training_data_input,training_data_output)
NBaccuracy = NBmodel.score(testing_data_input,testing_data_output)
predicted_output = NBmodel.predict(testing_data_input)
print "MultinomialNB : "+str(NBaccuracy*100.0)
generate_confusion_matrix(testing_data_output,predicted_output,models[2])
accuracies.append(NBaccuracy * 100.0)

NBmodel = BaggingClassifier(MultinomialNB(),max_samples=1.0, max_features=1.0)
NBmodel.fit(training_data_input,training_data_output)
NBaccuracy = NBmodel.score(testing_data_input,testing_data_output)
predicted_output = NBmodel.predict(testing_data_input)
print "Bagging MultinomialNB : "+str(NBaccuracy*100.0)
generate_confusion_matrix(testing_data_output,predicted_output,models[3])
accuracies.append(NBaccuracy * 100.0)

DTmodel = DecisionTreeClassifier()
DTmodel.fit(training_data_input,training_data_output)
DTaccuracy = DTmodel.score(testing_data_input,testing_data_output)
predicted_output = DTmodel.predict(testing_data_input)
print "Decision Tree : "+str(DTaccuracy*100.0)
generate_confusion_matrix(testing_data_output,predicted_output,models[4])
accuracies.append(DTaccuracy * 100.0)

DTmodel = BaggingClassifier(DecisionTreeClassifier(),max_samples=1.0, max_features=1.0)
DTmodel.fit(training_data_input,training_data_output)
DTaccuracy = DTmodel.score(testing_data_input,testing_data_output)
predicted_output = DTmodel.predict(testing_data_input)
print "Bagging Decision Tree : "+str(DTaccuracy*100.0)
generate_confusion_matrix(testing_data_output,predicted_output,models[5])
accuracies.append(DTaccuracy * 100.0)

LinearSVCmodel = LinearSVC()
LinearSVCmodel.fit(training_data_input,training_data_output)
LinearSVCaccuracy = LinearSVCmodel.score(testing_data_input,testing_data_output)
predicted_output = LinearSVCmodel.predict(testing_data_input)
print "Linear SVC : "+str(LinearSVCaccuracy*100.0)
generate_confusion_matrix(testing_data_output,predicted_output,models[6])
accuracies.append(LinearSVCaccuracy * 100.0)

LinearSVCmodel = BaggingClassifier(LinearSVC(),max_samples=1.0, max_features=1.0)
LinearSVCmodel.fit(training_data_input,training_data_output)
LinearSVCaccuracy = LinearSVCmodel.score(testing_data_input,testing_data_output)
predicted_output = LinearSVCmodel.predict(testing_data_input)
print "Bagging  Linear SVC : "+str(LinearSVCaccuracy*100.0)
generate_confusion_matrix(testing_data_output,predicted_output,models[7])
accuracies.append(LinearSVCaccuracy * 100.0)

SVCmodel = SVC()
SVCmodel.fit(training_data_input,training_data_output)
SVCaccuracy = SVCmodel.score(testing_data_input,testing_data_output)
predicted_output =SVCmodel.predict(testing_data_input)
print "SVC : "+str(SVCaccuracy*100.0)
generate_confusion_matrix(testing_data_output,predicted_output,models[8])
accuracies.append(SVCaccuracy * 100.0)

SVCmodel = BaggingClassifier(SVC(),max_samples=1.0, max_features=1.0)
SVCmodel.fit(training_data_input,training_data_output)
SVCaccuracy = SVCmodel.score(testing_data_input,testing_data_output)
predicted_output =SVCmodel.predict(testing_data_input)
print "Bagging SVC : "+str(SVCaccuracy*100.0)
generate_confusion_matrix(testing_data_output,predicted_output,models[9])
accuracies.append(SVCaccuracy * 100.0)

plotter(accuracies,models)

