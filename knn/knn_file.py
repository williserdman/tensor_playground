
import pandas as pd
import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import numpy
from sklearn import linear_model, preprocessing

data = pd.read_csv("~/Documents/coding/tensor_playground/knn/car.data")

#Converts text data into numerical
le = preprocessing.LabelEncoder()
#Creates numpy array for each of these
buying = le.fit_transform(list(data["buying"]))
maint = le.fit_transform(list(data["maint"]))
door = le.fit_transform(list(data["door"]))
persons = le.fit_transform(list(data["persons"]))
lug_boot = le.fit_transform(list(data["lug_boot"]))
safety = le.fit_transform(list(data["safety"]))
clss = le.fit_transform(list(data["class"]))

predict = "class"

#Taking these arrays and converting them into lists
x = list(zip(buying, maint, door, persons, lug_boot, safety))
y = list(clss)#y is result

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

print(x_train)
print(x_test)
print(y_train)
print(y_test)

