import pandas as pd
import numpy as np
import os
import shutil 
import librosa as lib
import soundfile as sf

def extract_filenames(path,key):
    '''
    Parameters
    ----------
    path : str
        path of audio script file.
    key : str
        keyword that we want to be extracted.

    Returns
    -------
    saves a csv file containing path of audio files that contained the keyword.

    '''
    df = pd.read_table(path)
    ll = []
    for i in range(len(df)):
        print(str(np.round( (i/len(df))*100,2) ) + ' % completed')
        l = df.iloc[i]['sentence'].split(' ')
        if key in l:
            ll.append(df.iloc[i]['path'])
    ll = pd.DataFrame(ll)
    ll.to_csv('E://project//data2//'+key+'.csv',index = False )
    
    
    

def move_filenames(keys_path,dest_path,files_path):
    '''
    Parameters
    ----------
    keys_path : str
        csv file containing keyword filenames.
    dest_path : str
        name of destination folder.
    files_path : str
        path of audio files.
    Returns
    -------
    moves all files that contain the keyword to a seperate folder.

    '''
    df = pd.read_csv(keys_path)['0'].values.tolist()
    list1 = os.listdir(files_path)
    for i in range(len(list1)):
        print(str( np.round((i/len(list1))*100,2) ) + '% completed.')
        if list1[i] in df:
            shutil.move('E://project//data2//validated//'+list1[i],'E://project//data2//'+dest_path)
        
        
    
    
    
extract_filenames('E://project//data2//cv-corpus-10.0-2022-07-04//fa//validated.tsv', 'سلام')
move_filenames('E://project//data2//سلام.csv', 'E://project//data2//سلام', 'E://project//data2//validated')
    
    


signal,sr = librosa.load('filename.wav')
    