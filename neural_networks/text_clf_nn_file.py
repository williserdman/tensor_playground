
import re
from token import ENCODING
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

#Changing working directory
#os.chdir("neural_networks\model.h5")

data = keras.datasets.imdb

(feature_train, target_train), (x_test, y_test) = data.load_data(num_words=88000) #only 10k most frequent words #this line splits it equally#changed to 88k

#print(feature_train[0])#prints reviews where a integer points to a word

word_index = data.get_word_index()#gives tuples that have the string and the word in them
word_index = {k:(v+3) for k, v in word_index.items()}
word_index['<PAD>'] = 0 #add padding to make every review be the same length with the hopes that it will be ignored
word_index['<START>'] = 1
word_index['<UNK>'] = 2
word_index['<UNUSED>'] = 3

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])#swaps values and keys, have integer pointing toward word instead of vice-versa

#Making the lenght of every review the same, can do this manually if you want (I didn't)
feature_train = keras.preprocessing.sequence.pad_sequences(feature_train, value=word_index['<PAD>'], padding='post', maxlen=256)
x_test = keras.preprocessing.sequence.pad_sequences(x_test, value=word_index['<PAD>'], padding='post', maxlen=256)

def decoder(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])#the "?" in get is a default values trying to prevent crashes. the space before .join puts a space between words

review = ["bad", "good"]

'''
#Making the model:
#16 is an arbitrary number of neurons
model = keras.Sequential()#We're gonna have more layers, so adding them in the next function instead of in a list like: Sequential([layers])
model.add(keras.layers.Embedding(88000, 16))#initially creates 10k word vectors, 16 dimensions/coefficients(ax+by+cz...). embedding layer takes the word vectors for the data we have and passes the word vectors to the next layer. looks at context at which its used
model.add(keras.layers.GlobalAveragePooling1D())#averages coefficients basically. 16 dimensions is a lot, so this scales it down a little bit. takes the dimension that's passed and turns it down
model.add(keras.layers.Dense(16, activation='relu'))#relu makes negatives 0 and positives more positive i think?? **CHECK** anyways it looks for patterns and tries to classify as pos. or neg. 
model.add(keras.layers.Dense(1, activation='sigmoid'))#sigmoid "squishes" everything between 0 and 1
#Going to have 1 output neuron, something like 1 good 0 bad

#model.summary()

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])#look up things here if wanted

x_val = feature_train[:10000]#validation data, size doesn't really matter.
x_train = feature_train[10000:]
#checks how well the model is doing after the first 10k dato points?
y_val = target_train[:10000]
y_train = target_train[10000:]

fitModel = model.fit(x_train, y_train, epochs=35, batch_size=512, validation_data=(x_val, y_val), verbose=1)#batch size is how many movie reviews are loaded at once

result = model.evaluate(x_test, y_test)
print(result)

model.save("model.h5", "~/Documents/coding/tensor_playground/neural_networks/")#h5 is the saved model for keras and tensorflow
'''#model's been run once, and have saved it so commenting this all out as we don't need to train the model again

model = keras.models.load_model("neural_networks\model.h5")#allows you to tweak hyper-parameters and save only the best one#the files are messed up big time, has to do with current working directory

def review_encode(in_string):
    encoded = [1]#all other data starts with 1
    for word in in_string:
        try:
            encoded.append(word_index[word.lower()])#tries adding the word by throwing it in the dictionary, if there's an error:
        except:
            encoded.append(2)#2 is the unknown tag
    return encoded

#Inputting a review
with open("neural_networks\\review.txt", 'r') as f:#no fucking clue whats going on rn, cant define path anymore?#got it! use "relative path"
    for line in f.readlines():#only one line (text wrapped, but makes easy if there are more reviews)
        #Have to convert string to numbers
        nline = line.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(":", "").replace("\"","").strip().split(" ")#removes random characters, prob better way to do this
        encoded = review_encode(nline)
        encoded = keras.preprocessing.sequence.pad_sequences([encoded], value=word_index['<PAD>'], padding='post', maxlen=256)
        preditciton = model.predict(encoded)
        print(line)
        print(preditciton, end='\n\n')

