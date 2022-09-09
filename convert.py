# convert mp3 to wav files

#sound = AudioSegment.from_mp3(path.normpath('E:\\project\\folder\\clips\\common_voice_fa_18202354.mp3') )
#sound.export('test.wav',format='wav')
  
    
from os import path
import subprocess

subprocess.call(['ffmpeg', '-i', 'common_voice_fa_18202354.mp3',
                 'file.wav'],shell=True)
