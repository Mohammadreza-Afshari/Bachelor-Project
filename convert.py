# convert mp3 to wav files
   
from os import path
import subprocess

subprocess.call(['ffmpeg', '-i', 'common_voice_fa_18202354.mp3',
                 'file.wav'],shell=True)
