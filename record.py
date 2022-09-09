import sounddevice as sd
from scipy.io.wavfile import write
import keyboard as kb
import os



def record(num,sr=22050,seconds=1):
    '''
    Parameters
    ----------
    num : int
        number of audio files to be recorded in this function call.
    sr : int, optional
        recording sample rate. The default is 22050.
    seconds : int, optional
        duration of each recording. The default is 1.

    Returns
    -------
    saves recorded files in the same directory as the code.
    '''
    
    list1 = os.listdir(os.getcwd())
    c = 0
    for i in list1:
        if i.split('.')[0][0:7] == 'keyword' and int(i.split('.')[0][8]) > c:
            c = int(i.split('.')[0][8])
            
    c += 1
    for i in range(num):
        while True:
            print('press "S" to start recording:')
            if kb.read_key() == 's':
                print(str(seconds) + ' second started.')
                myrecording = sd.rec(int(seconds * sr), samplerate=sr, channels=2)
                sd.wait() 
                write('keyword_' + str(c)+'.wav', sr, myrecording) 
                print('recorded file number '+str(c))
                print('-------------------------------------------------------------')
                c += 1
                break        


record(1,seconds=60)



