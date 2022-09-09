import librosa as lib
import numpy as np
import os
import soundfile as sf
import shutil


def noise(sig,noise_factor):
    '''
    Parameters
    ----------
    sig : numpy array of audio signal
    noise_factor : float [0,1]
        significance of noise.

    Returns
    -------
    augmented_data : numpy array of augmented audio signal.
        returns the audio signal with random nois added to it.

    '''
    noise = np.random.randn(len(sig))
    augmented_data = sig + noise_factor * noise
    augmented_data = augmented_data.astype(type(sig[0]))
    return augmented_data





def pitch(sig,sr,pitch_factor):
    '''
    Parameters
    ----------
    sig : numpy array of audio signal
        
    sr : int
        sample rate
    pitch_factor : float [0,1]

    Returns
    -------
    numpy array of pitch shifted audio signal
        

    '''
    return lib.effects.pitch_shift(sig, sr, pitch_factor)





def extend(path,sample_rate):
    '''
    extends audio files by adding silence to reach 1 second of duration based on sample rate

    Parameters
    ----------
    path : str
        path of the folder containing audio files
    sample_rate : int
        sample rate of audio files 

    Returns
    -------
    None.

    '''
    li = os.listdir(path)
    for i in li:
        if len(i.split('.')) > 1 and i.split('.')[1] == 'wav':
            data,sr = lib.load(path+'\\'+i)
            data = list(data)
            short = sample_rate - len(data)
            left = np.random.randint(0,short)
            left = np.zeros(left)
            left = list(left)
            right = np.zeros(short-len(left))
            right = list(right)
            final = []
            final.append(left)
            final.append(data)
            final.append(right)
            f2 = []
            for j in final:
                for k in j:
                    f2.append(k)
            f2 = np.array(f2)
            sf.write(path+'\\extended\\'+i.split('.')[0]+'_ext.wav',f2,sample_rate)






def upsample(path=None):
    '''
    up-samples the dataset by augmenting new data from existing audio files in the path.
    
    Parameters
    ----------
    path : str
        path of audio files.

    Returns
    -------
    up-samples the dataset and saves new files in "augmented" folder.

    '''
    
    list1 = os.listdir(path)
    
    for x in list1:
        if 'wav' not in x.split('.'):
            continue
        
        sig,sr = lib.load(path+'\\'+x)
        noisy = []
        pitchy = []
        for j in range(2):
            fac = np.random.uniform(low=0.0, high=0.0009)
            n_steps = np.random.uniform(-2,2)
            noisy.append(noise(sig,fac))
            pitchy.append(pitch(sig,sr,n_steps))
        
        # save augmented audio files    
        name = x.split('.')[0]
        for i in range(len(noisy)):
            for k in range(2):
                sf.write(path+'//augmented//4//'+name+'_noise_'+str(i)+'_'+str(k)+'.wav',noisy[i],22050)
                sf.write(path+'//augmented//4//'+name+'_pitch_'+str(i)+'_'+str(k)+'.wav',pitchy[i],22050)
                sf.write(path+'//augmented//4//'+name+'_replicated_'+str(k)+'.wav',sig,22050)






def slice_datasets(path):
    '''
    slice the datasets into 3 parts randomly

    Parameters
    ----------
    path : str
        path of the folder containing audio files

    Returns
    -------
    None.

    '''
    li = os.listdir(path)
    for i in li:
        if 'wav' not in i.split('.') and 'mp3' not in i.split('.'):
            continue
        rand = np.random.randint(0,100)
        if rand <= 33:
            shutil.move(path+'//'+i,path+'//11')    
        elif rand <= 66:
            shutil.move(path+'//'+i,path+'//22')
        else:
            shutil.move(path+'//'+i,path+'//33')
    











#extend('E:\\project\\data2\\salam_true',22050)
upsample('E:\\project\\data2\\test')
#slice_datasets('E://project//data2//test//augmented')


