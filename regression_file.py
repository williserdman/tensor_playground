
import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle

#Reading this data using pandas, delimiter (the same as sep) is a semicolon for some reason, so it's specified. 
data = pd.read_csv("student-mat.csv", sep=';')
#print(data.head())#The .head() prints only the first 5 values

#Specifying the data that we actually want to process (just these six are going to be taken into account)
data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]

to_be_predicted = "G3"

attribute_array = np.array(data.drop([to_be_predicted], 1))#why , 1?
label_array = np.array(data[to_be_predicted])#results, the value of G3

#Taking attributes and labels (in arrays above) and splitting them up into 4 different arrays. Both attribute_train and label_train will be sections of the respective arrays. The test data will test the accuracy of the algorithm/model. 10% of the data (or 0.1) will be reserved for "test samples"
attribute_train, label_train, attribute_test, label_test = sklearn.model_selection.train_test_split(attribute_array, label_array, test_size=0.1)
