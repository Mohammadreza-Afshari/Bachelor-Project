import tensorflow.keras as keras
import numpy as np
import librosa
import matplotlib.pyplot as plt
import os


mapping = ['false','true']
out = []
#load the model
model = keras.models.load_model('E:\\project\\data2\\test2\\1\\model.h5')

def predict(filepath):
    signal, sr = librosa.load(filepath)
    
    if len(signal) != 22050:
        return
    
    signal = signal[:22050]   
    mfcc = librosa.feature.mfcc(y=signal,sr=22050,n_mfcc=13,n_fft=2048,hop_length=512).T
    #plt.Figure(figsize=(10,20),dpi=400)
    #plt.imshow(librosa.power_to_db(mfcc.T**2))
    #  (# of samples, # of segments, # of coefs, # of channels)
    mfcc = mfcc[np.newaxis, ...,np.newaxis ]
    # rnn
    #mfcc = mfcc[np.newaxis, ...]
    preds = model.predict(mfcc)
    idx = np.argmax(preds)
    print('predicted keyword is ',end='')
    print(mapping[idx])
    


li = os.listdir('E:\\project\\data2\\test2\\tt') 
for i in li:
    print(i+' :')
    predict('E:\\project\\data2\\test2\\tt\\'+i)








