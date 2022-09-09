import json
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras 
import pandas as pd





path = 'E:\\project\\data2\\test\\augmented\\5'



def prepare_data(path):

    with open(path) as f:
        data = json.load(f)
    X = data['MFCC']
    y = data['labels']
    X = np.array(X)
    y = np.array(y)
    X_train, X_test, Y_train, Y_test = train_test_split(X,y,test_size=0.1)
    X_train, X_val, Y_train,Y_val = train_test_split(X_train,Y_train,test_size=0.1)
    return (X_train,X_test,Y_train,Y_test,X_val,Y_val)




#-------------- loading the data -----------------------
(X_train,X_test,Y_train,Y_test,X_val,Y_val) = prepare_data(path+'\\data.json')
# adding number of channels to our data ( so far the data is: [# of segments,# coefs])
X_train = X_train[...,np.newaxis]
X_test = X_test[...,np.newaxis]
X_val = X_val[...,np.newaxis]






#********************************************* build the model ***************************************************
input_shape = (X_train.shape[1], X_train.shape[2], X_train.shape[3])  # ( # of segments, # of coefs, # of channels)
learning_rate = 0.0001

model = keras.Sequential()

#conv layer 1
model.add(keras.layers.Conv2D(32, (3,3), activation='relu', 
          input_shape=input_shape,kernel_regularizer=keras.regularizers.l2(0.005)))

model.add(keras.layers.BatchNormalization())
model.add(keras.layers.MaxPool2D( (2,2), strides=(2,2) , padding='same' ))

#conv layer 2
model.add(keras.layers.Conv2D(16, (2,2), activation='relu', 
          kernel_regularizer=keras.regularizers.l2(0.005)))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.MaxPool2D( (2,2), strides=(2,2) , padding='same' ))



# dense layer
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(32, activation='relu'))
model.add(keras.layers.Dropout(0.5))

#softmax
model.add(keras.layers.Dense(2,activation='softmax'))

#compile
optimiser = keras.optimizers.Adam(learning_rate)
model.compile(optimizer = optimiser, loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model.summary()


#********* train the model

model.fit(X_train, Y_train, epochs = 10, batch_size = 32, validation_data = (X_val,Y_val))

loss = pd.DataFrame(model.history.history)
loss.plot()

#********* model performance
loss , accuracy = model.evaluate(X_test,Y_test)
print('test error:',end=' ')
print(loss)
print('test accuracy: ',end='')
print(accuracy)


#save model
model.save(path+'\\model.h5')





















# RNN-LSTM model 
input_shape = (X_train.shape[1], X_train.shape[2])  # ( # of segments, # of coefs, # of channels)
learning_rate = 0.0001

model = keras.Sequential()
# seq-to-seq
model.add(keras.layers.LSTM(45, input_shape=input_shape))
model.add(keras.layers.Dense(32,activation='relu'))
model.add(keras.layers.Dropout(0.35))
#softmax
model.add(keras.layers.Dense(2,activation='softmax'))
#compile
optimiser = keras.optimizers.Adam(learning_rate)
model.compile(optimizer = optimiser, loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model.summary()




#********* train the model
model.fit(X_train, Y_train, epochs = 15, batch_size = 32, validation_data = (X_val,Y_val))

loss = pd.DataFrame(model.history.history)
loss.plot()

#********* model performance
loss , accuracy = model.evaluate(X_test,Y_test)
print('test error:',end=' ')
print(loss)
print('test accuracy: ',end='')
print(accuracy)

#save model
model.save(path+'//rnnmodel.h5')
