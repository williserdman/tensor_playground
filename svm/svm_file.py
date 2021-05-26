
#support vector machine. uses a kernel (random formula) and applies it to every point on a(n imaginary) graph, with the hopes that one data set will split from another. if they do, one can draw a line through (hyperplane), and guess each side corresponding to a different result
import sklearn
from sklearn import datasets, svm, metrics
from sklearn.neighbors import KNeighborsClassifier

cancer = datasets.load_breast_cancer()#data from sklearn

x = cancer.data
y = cancer.target

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)
names = ["malignant", "benign"]

model = svm.SVC()#svc likely mean: support vector classification/classifier #C is the soft-margin#linear is the same as knn
knn_model = KNeighborsClassifier(n_neighbors = 11)#always test different options/models

model.fit(x_train, y_train)
knn_model.fit(x_train, y_train)

prediction = model.predict(x_test)
knn_prediction = knn_model.predict(x_test)

acc = metrics.accuracy_score(y_test, prediction)
knn_acc = metrics.accuracy_score(y_test, knn_prediction)
print(acc)
print(knn_acc)
