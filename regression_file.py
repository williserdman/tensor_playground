
from numpy.lib.function_base import average
import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle

def calculation():
    #Reading this data using pandas, delimiter (the same as sep) is a semicolon for some reason, so it's specified. 
    data = pd.read_csv("student-mat.csv", sep=';')
    #print(data.head())#The .head() prints only the first 5 values

    #Specifying the data that we actually want to process (just these six are going to be taken into account)
    data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]

    to_be_predicted = "G3"

    attribute_array = np.array(data.drop([to_be_predicted], 1))#why , 1?
    label_array = np.array(data[to_be_predicted])#results, the value of G3

    #Taking attributes and labels (in arrays above) and splitting them up into 4 different arrays. Both attribute_train and label_train will be sections of the respective arrays. The test data will test the accuracy of the algorithm/model. 10% of the data (or 0.1) will be reserved for "test samples"
    #Where sklearn is taking in two data points, the attribute_array=x and label_array=y it'll be placed on a graph to find the line of best fit
    #We have more than 2 variables, so have to make a multi-dimensional line of best fit, using multiple variables
    attribute_train, attribute_test, label_train, label_test = sklearn.model_selection.train_test_split(attribute_array, label_array, test_size=0.1)

    line_of_best_fit = linear_model.LinearRegression()

    #This is actually finding the line of best fit (attribute_train=x and label_train=y)
    line_of_best_fit.fit(attribute_train, label_train)

    #Returns accuracy of model
    accuracy = line_of_best_fit.score(attribute_test, label_test)

    return accuracy #varies

    #With 5 variables it's in 5d space, so there are 5 coefficients
    print(line_of_best_fit.coef_)
    print(line_of_best_fit.intercept_)

    prediction = line_of_best_fit.predict(attribute_test)

    for i, l in enumerate(prediction):
        print(prediction[i], attribute_test[i], label_test[i])

try:
    times_run = int(input("how many times do you want to run the linear regression model to fin accuracy? (int): "))
except ValueError:
    print("thats not an int, silly")

avg_accuracy = 0
for i in range(times_run):
    avg_accuracy += calculation()

avg_accuracy = avg_accuracy/times_run

print(avg_accuracy*100, '%')#ran 1000 times, 82.5% accuracy on average