
from numpy.lib.function_base import average
import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style

def calculation():
    #Reading this data using pandas, delimiter (the same as sep) is a semicolon for some reason, so it's specified. 
    data = pd.read_csv("~/Documents/coding/tensor_playground/linear_regression/student-mat.csv", sep=';')
    #print(data.head())#The .head() prints only the first 5 values
    
    #Specifying the data that we actually want to process (just these six are going to be taken into account)
    data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]

    to_be_predicted = "G3"

    attribute_array = np.array(data.drop([to_be_predicted], 1))#why , 1?
    label_array = np.array(data[to_be_predicted])#results, the value of G3

    attribute_train, attribute_test, label_train, label_test = sklearn.model_selection.train_test_split(attribute_array, label_array, test_size=0.1)

    '''
    #The next for loop is creating a model. Once a model is created, doesn't have to be run again, preferable in its own function
    best_acc = 0 #Getting high accuracy model
    for i in range(100):
        #Taking attributes and labels (in arrays above) and splitting them up into 4 different arrays. Both attribute_train and label_train will be sections of the respective arrays. The test data will test the accuracy of the algorithm/model. 10% of the data (or 0.1) will be reserved for "test samples"
        #Where sklearn is taking in two data points, the attribute_array=x and label_array=y it'll be placed on a graph to find the line of best fit
        #We have more than 2 variables, so have to make a multi-dimensional line of best fit, using multiple variables
        attribute_train, attribute_test, label_train, label_test = sklearn.model_selection.train_test_split(attribute_array, label_array, test_size=0.1)

        line_of_best_fit = linear_model.LinearRegression()

        #This is actually finding the line of best fit (attribute_train=x and label_train=y)
        line_of_best_fit.fit(attribute_train, label_train)

        #Accuracy of model, varies
        accuracy = line_of_best_fit.score(attribute_test, label_test)
        print(accuracy)

        if accuracy > best_acc:
            best_acc = accuracy
            #Saving our model, if there's one with a really high accuracy for example, as they all train slightly differently. Or for larger data sets you don't want to have to re-train your model.
            with open("studentmodel.pickle", 'wb') as pickle_file:
                pickle.dump(line_of_best_fit, pickle_file)'''
    #print(best_acc)
    with open("studentmodel.pickle", 'rb') as pickle_input:
        line_of_best_fit = pickle.load(pickle_input)
    
    #With 5 variables it's in 5d space, so there are 5 coefficients
    #print(line_of_best_fit.coef_)
    #print(line_of_best_fit.intercept_)

    prediction = line_of_best_fit.predict(attribute_test)

    for i, l in enumerate(prediction):
        print(prediction[i], attribute_test[i], label_test[i])

    one_attribute = "G1"
    style.use("ggplot")
    #Creates a scatterplot, where one attribute is the x val. The y val is the label/result/G3
    pyplot.scatter(data[one_attribute], data["G3"])
    pyplot.xlabel(one_attribute)
    pyplot.ylabel("Final Grade")
    pyplot.show()

calculation()
