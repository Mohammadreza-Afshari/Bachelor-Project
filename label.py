import os
import librosa
import soundfile as sf
import pandas as pd
import numpy as np
from pydub import AudioSegment
import simpleaudio
import shutil





def cut_audio(path,sr=22050):
    '''
    Parameters
    cuts audio files into 0.6 seconds intervals by hop length = 0.5 seconds
    and stores it in "cut" folder
    ----------
    path : str
        path of the folder containing audio files
    sr : int, optional
        sample rate. The default is 22050.

    Returns
    -------
    None.
    '''
    
    li = os.listdir(path)
    dir1 = os.getcwd()
    
    for i in li:
        df,sr = librosa.load(path+'//'+i)
        c = 0
        for j in range(0,len(df),11025):    # hop by 5/10 of sample rate
            if j + 13230 < len(df):    # 0.6 seconds
                df1 = df[j:j+13230]
                sf.write(path+'//cut//'+i.split('.')[0]+'#'+str(c)+'.wav',df1,22050)
                c += 1
            
        





def label_sounds(path):
    '''
    plays each audio file and asks you for its label
    
    Parameters
    ----------
    path : str
        path of the folder containing our audio files

    Returns
    -------
    None.

    '''
    li = os.listdir(path)
    trues = []
    for i in range(len(li)):
        print(np.round(i/len(li) * 100,2))
        audio = AudioSegment.from_wav(path+'//'+li[i])
        playback = simpleaudio.play_buffer(
                audio.raw_data, 
                num_channels=audio.channels, 
                bytes_per_sample=audio.sample_width, 
                sample_rate=audio.frame_rate
                )
        
        p = input('please enter the label for the above audio:')
        if p == '1':
            playback.stop()
            trues.append(li[i])
            print(trues)
        else:
            playback.stop()
        print('-------------------------------')
        print()
        
    df = pd.DataFrame(trues)
    df.to_csv('extracted_trues.csv',index=False)
        
        








#cut_audio('E:\project\\data2\\ساعت')       
label_sounds('E:\project\\data2\\ساعت\\cut')




# move files
'''
l = pd.read_csv('extracted_trues.csv').values.tolist()
for i in l:
    shutil.move('E://project//data2//سلام//cut//'+i[0],'E://project//data2//salam_true')
'''






