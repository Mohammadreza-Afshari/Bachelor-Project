import librosa
import soundfile as sf 


frames , sr = librosa.load('sounds//F29W01.wav')
import librosa.display
import matplotlib.pyplot as plt

l = []
for i in range(0,len(frames),10000):
    l.append(frames[i:i+11025])
print(len(l))


import numpy as np

for i in range(len(l[2])):
    if np.random.randint(80,120) == 85:
        l[2][i] = 0
        l[3][i] = 0
        l[4][i] = 0






sf.write('stereo_file.wav', l[2], 22050, subtype='PCM_24')
sf.write('stereo_file2.wav', l[3], 22050, subtype='PCM_24')
sf.write('stereo_file3.wav', l[4], 22050, subtype='PCM_24')

t = librosa.frames_to_time(range(0,len(frames)),hop_length=5000,sr=22050)
plt.figure(figsize=(10,5),dpi=400)

hop = 10000

plt.plot(t[0:11025],frames[0:11025],alpha=0.3,c='r')
plt.plot(t[hop+1:hop+1+11025],frames[hop+1:hop+1+11025],alpha=0.3,c='b')














