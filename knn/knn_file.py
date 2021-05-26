
#k nearest neighbors, k is a variable, the number of neighbors to look for. this is very computationally heavy, and the time it takes to compute will linearly increase
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
stlye = le.fit_transform(list(data["style"]))

predict = "stlye"

#Taking these arrays and converting them into lists
x = list(zip(buying, maint, door, persons, lug_boot, safety))
y = list(stlye)#y is result

#Anything with train in it, are used for training. x_train would be the input for training, and to check its work y_train would be used. That means that the model already knows those values, so should have 100% accuracy. x_test and y_test follow the same idea, but the model has never seen them before. 
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

model = KNeighborsClassifier(n_neighbors = 9)

model.fit(x_train, y_train)
acc = model.score(x_test, y_test)
print(acc)

prediction = model.predict(x_test)
names = ["unacc", "acc", "good", "vgood"]

for i, l in enumerate(x_test):
    print(names[prediction[i]], end = ' | ')
    print(l, end = ' | ')
    print(names[y_test[i]], end = ' | ')
    model.kneighbors([x_test[i]], 9)#kneighbors takes a 2 dimensional array, so we have to turn our input into one


