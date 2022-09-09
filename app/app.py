import pyaudio
import numpy as np
from librosa import load
from librosa.feature import mfcc as mf
import time
import soundfile as sf
import tensorflow.keras as keras
import matplotlib.pyplot as plt
from threading import Thread
import os

record = False


 
widgets = {
    'record_start_button':[],
    'record_stop_button':[],
    'recorder_heading':[],
    'record_description':[],
    'record_status':[]
}



class Recorder:
    def __init__(self, sample_rate=22050, record_seconds=1):
        self.model = keras.models.load_model('model.h5')
        self.queue = list()
        self.chunk = 1050
        self.sample_rate = sample_rate
        self.record_seconds = record_seconds
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=self.chunk)

    def listen(self):
        global record
        global graph
        while record:
            #print('started recording')
            # change this to button press
            '''
            if kb.is_pressed('s'):
                break
            '''
            data = self.stream.read(self.chunk , exception_on_overflow=False)
            self.queue.append(np.frombuffer(data,dtype=np.float32))
            time.sleep(0.01)
        return self.queue
    
    def predict(self,path=''):

        if path != '':
            widgets['record_status'][-1].setText('Status: Processing')
            data,_ = load(path)
        else:
            widgets['record_status'][-1].setText('Status: Listening')
            data = self.listen()
            data = np.array(data).flatten()
        ds = []
        # chop up the recorded audio into 1 second signals by hop size = 0.5 seconds
        for i in range(0,len(data),1024):
            if i + 22050 <= len(data):
                ds.append (data[i:i+22050])
        preds = []
        for i in ds:
            mfcc = mf(y=i,sr=22050,n_mfcc=13,n_fft=2048,hop_length=512).T
            mfcc = mfcc[np.newaxis, ..., np.newaxis ] 
            preds.append(np.argmax(self.model.predict(mfcc)))

        self.visualize(data,preds)
    


    def visualize(self,data,predictions):
        fig,ax = plt.subplots(figsize=(10,5))
        ax.set_title('Audio Signal')
        ax.set_xlabel('time')
        ax.set_ylabel('amplitude')
        ax.set_facecolor((0.01,0,0.02))
        ax.plot(np.arange(len(data)),data,color='white',lw=0.7)
        for i in range(len(predictions)):
            if predictions[i] == 1:
                y = data[i*1024:i*1024+22050]
                sf.write(os.getcwd()+'\\'+str(i)+'.wav',y,22050)
                x = np.arange(i*1024,i*1024+22050)
                if i == 0:
                    ax.plot(x,y,color='green',lw=0.7) 
                else:
                    ax.plot(x,y,color='green',lw=0.7)

        fig.savefig(os.getcwd()+'\\1.png',dpi=500/fig.get_size_inches()[1])







#------------------------- callback functions for gui ------------------------------------------

def start_recorder(path=''):
    recorder = Recorder()
    recorder.predict(path=path)




def end_loop(ispath=False):
    global record
    if record == False and ispath == False:
        return
    if record:
        record = False
    widgets['record_status'][-1].setText('Status: Waiting')
    image = 'loading'
    while True:
        if '1.png' in os.listdir():
            break
    time.sleep(0.7)
    image = QPixmap('1.png')
    plot = QLabel()
    plot.setPixmap(image)
    plot.setAlignment(QtCore.Qt.AlignCenter)
    plot.setStyleSheet('margin-top:20px;')
    grid.addWidget(plot,4,0,2,3)
    os.remove(os.getcwd()+'\\1.png')


def start_recording(path):
    global record
    if record:
        return
    record = True
    t1 = Thread(target=start_recorder, daemon=True)
    t1.start()



def dialog():
    file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                               "", "All Files (*)")

    print(file)
    if check:
        start_recorder(file)


def show_results():
    end_loop(True)




# ------------------------------------- GUI ---------------------------------------------
import sys
from PyQt5.QtWidgets import QApplication, QLabel,QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout,QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor




app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Keyword Detector')
window.setFixedWidth(1100)
window.setFixedHeight(800)
window.setStyleSheet(
    "background: #161219;"
)

grid = QGridLayout()




# ----------------------------- recording page ------------------------------
def recording_frame():

    #page heading
    heading = QLabel('Recorder')
    heading.setAlignment(QtCore.Qt.AlignCenter)
    heading.setStyleSheet(
        '''
            font-size:30px;
            color:white;
            border-bottom: 1px solid white;
            padding-bottom:10px;
            font-weight:bold;
        '''
    )
    widgets['recorder_heading'].append(heading)


    # page description
    desc = QLabel('Click on "start recording" to record your voice and when you are finished click on "stop recording" in order to see all the detected keywords. You also can select a local audio file(.wav file) to be processed.')
    desc.setAlignment(QtCore.Qt.AlignCenter)
    desc.setWordWrap(True)
    desc.setStyleSheet('''
        font-size:18px;
        color:white;
    ''')
    widgets['record_description'].append(desc)



    #start recording button
    startbutton = QPushButton('Start Recording')
    startbutton.setStyleSheet('''
        *{
        margin:10px;
        border-radius:10px;
        padding:10px;
        color:white;
        border:2px solid green;
        font-size: 16px;
        max-width:150px;
        }
        *:hover{
            background:green;
        }
    ''')
    startbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    startbutton.clicked.connect(start_recording)
    widgets['record_start_button'].append(startbutton)


    #stop recording button
    stopbutton = QPushButton('Stop Recording')
    stopbutton.setStyleSheet('''
        *{
        margin:10px;
        border-radius:10px;
        padding:10px;
        color:white;
        font-size: 16px;
        max-width:150px;
        border: 2px solid red;
        }
        *:hover{
        background:red;
        }
    ''')
    stopbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    stopbutton.clicked.connect(end_loop)
    widgets['record_stop_button'].append(stopbutton)




    #select file button
    button = QPushButton('Select File')
    button.setStyleSheet('''
        *{
        margin:10px;
        border-radius:10px;
        padding:10px;
        color:white;
        font-size: 16px;
        max-width:150px;
        border: 2px solid white;
        }
        *:hover{
        background:white;
        color:black
        }
    ''')
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(dialog)


    #process file button
    button2 = QPushButton('Process File')
    button2.setStyleSheet('''
        *{
        margin:10px;
        border-radius:10px;
        padding:10px;
        color:white;
        font-size: 16px;
        max-width:150px;
        border: 2px solid white;
        }
        *:hover{
        background:white;
        color:black
        }
    ''')
    button2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button2.clicked.connect(show_results)
    




    # recording status
    stat = QLabel('Status: Waiting')
    stat.setAlignment(QtCore.Qt.AlignCenter)
    stat.setWordWrap(True)
    stat.setStyleSheet('''
        font-size:14px;
        color:white;
        font-weight:bold;
        border: 1px solid white;
        padding:5px;
        max-width:100px;
    ''')
    widgets['record_status'].append(stat)






    grid.addWidget(widgets['recorder_heading'][-1],0,0,1,3)
    grid.addWidget(widgets['record_description'][-1],1,0,1,3)
    grid.addWidget(widgets['record_start_button'][-1],2,0)
    grid.addWidget(widgets['record_stop_button'][-1],2,1)
    grid.addWidget(widgets['record_status'][-1],2,2)
    grid.addWidget(button,3,0)
    grid.addWidget(button2,3,1)
# -----------------------------------------------------------------------------


recording_frame()

window.setLayout(grid)

window.show()
sys.exit(app.exec())

