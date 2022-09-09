import librosa  
import os
import json
import numpy as np
import random


def chop_up(data):
    chops = []
    for j in range(0,len(data),11025):    # hop by 0.5 second
        if j + 22050 < len(data):    # 1 second
            data1 = data[j:j+22050]
            chops.append(data1)
    return chops



def create_dataset(path):

    data = {
            "map": ['false','true'],  # what keyword each number represent 
            "labels": [],     # label of each audio file
            "MFCC": [],       # MFCC of each audio file 
            "file": []        # path of each audio file
            }
            
    count = 0
    for i in range(len(data['map']) ):
        files = os.listdir(path+'//' + data['map'][i])
        random.shuffle(files)
        for f in files:
            filename = path+'//' + data['map'][i] + '//' + f
            print(filename)
            
            signal , sr = librosa.load(filename)
            if data['map'][i] == 'false' and len(signal) >= 22050:
                chps = chop_up(signal)
                count += len(chps)
                if count >= 6000:
                    break
                for c in range(len(chps)):
                    mfcc = librosa.feature.mfcc(chps[c], sr=22050, n_mfcc=13, hop_length=512, n_fft=2048) 
                    data['labels'].append(i)
                    data['MFCC'].append(mfcc.T.tolist())
                    data['file'].append(filename)
            elif len(signal)==22050:
                mfcc = librosa.feature.mfcc(signal, sr=22050, n_mfcc=13, hop_length=512, n_fft=2048) 
                data['labels'].append(i)
                data['MFCC'].append(mfcc.T.tolist())
                data['file'].append(filename)                
        
            
    with open(path+'//data.json','w') as f:
        json.dump(data,f,indent=4)
    
    
    
    
create_dataset('E://project//data2//test//augmented//4')


    
    
  