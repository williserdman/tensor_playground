
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as pyplot

data = keras.datasets.fashion_mnist #their dataset

(train_images, train_labels), (test_images, test_labels) = data.load_data()

#Getting these values between 0 and 1. The data is store in a numpy array, a 2d list where a number corresponds to a greyscale value
train_images = train_images/255
test_images = test_images/255

names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#print(train_images[0]) stored in a numpy array where a list corresponts to a row of pixels. images are only 28x28
#pyplot.imshow(train_images[0], cmap = pyplot.cm.binary)#will show the image input. to see it normally add cmap = plt.cm.binary
#pyplot.show()

#"Flattening the data" making a 1d list from 2d array. Will have 784 (28*28, the num of pixels) input neurons, and 10 output neurons representing the 10 options
#Using 1 hidden layer with 128 neurons, hidden layers dont really matter though
model = keras.Sequential([#means a sequence of layers, defined in order
    keras.layers.Flatten(input_shape=(28,28)),#input
    keras.layers.Dense(128, activation='relu'),#(dense) fully connected to the prev
    keras.layers.Dense(10, activation='softmax')#softmax for output will have the neurons sum to 100% certainty
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=5)#play with epochs, its the number of times the images are shown

#Using the model
prediction = model.predict([test_images])#you have to put what you want to be predicted inside a list (its expecting you to predict several things), for each input it returns a list of values (of the 10 neurons)

#Showing some images and then prediction
for i in range(5):
    pyplot.grid(False)
    pyplot.imshow(test_images[i], cmap=pyplot.cm.binary)
    pyplot.xlabel("Actual Label: " + names[test_labels[i]])
    pyplot.title("Prediction: " + names[np.argmax(prediction[i])])
    pyplot.show()
