import pyaudio
import threading
import time
import wave
import numpy as np
from threading import Event
import tensorflow.keras as keras
import tensorflow as tf
import librosa
import soundfile as sf


global graph
graph = tf.get_default_graph()


class Listener:

    def __init__(self, sample_rate=22050, record_seconds=2):
        self.chunk = 1050
        self.sample_rate = sample_rate
        self.record_seconds = record_seconds
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=self.chunk)

    def listen(self, queue):
        while True:
            data = self.stream.read(self.chunk , exception_on_overflow=False)
            queue.append(data)
            time.sleep(0.01)

    def run(self, queue):
        thread = threading.Thread(target=self.listen, args=(queue,), daemon=True)
        thread.start()
        print("\nWake Word Engine is now listening... \n")


class WakeWordEngine:

    def __init__(self, model_file):
        self.c = 0
        self.model = keras.models.load_model('E:\\project\\data2\\test\\augmented\\4\\model3.h5')
        self.listener = Listener(sample_rate=22050, record_seconds=2)
        self.audio_q = list()

    def save(self, waveforms, fname="wakeword_temp"):
        wf = wave.open(fname, "wb")
        # set the channels
        wf.setnchannels(1)
        # set the sample format
        wf.setsampwidth(self.listener.p.get_sample_size(pyaudio.paInt16))
        # set the sample rate
        wf.setframerate(22050)
        # write the frames as bytes
        wf.writeframes(b"".join(waveforms))
        # close the file
        wf.close()
        return fname


    def predict(self, audio):
        fname = self.save(audio)
        signal, _ = librosa.load(fname)  # don't normalize on train
        signal = signal[:22050]
        mfcc = librosa.feature.mfcc(y=signal,sr=22050,n_mfcc=13,n_fft=2048,hop_length=512).T
        mfcc = mfcc[np.newaxis, ..., np.newaxis ]

            # TODO: read from buffer instead of saving and loading file
            # waveform = torch.Tensor([np.frombuffer(a, dtype=np.int16) for a in audio]).flatten()
            # mfcc = self.featurizer(waveform).transpose(0, 1).unsqueeze(1)
        
        preds = self.model.predict(mfcc)
        idx = np.argmax(preds)
        if idx == 1:
            sf.write('C:\\Users\\LENOVO\\Desktop\\wavs\\'+str(self.c)+'.wav',signal,22050)
            self.c += 1
            print(str(self.c)+': ',end ='')
            print(idx)
        return idx

    def inference_loop(self, action):
        while True:
            if len(self.audio_q) > 21:  # remove part of stream
                diff = len(self.audio_q) - 21
                for _ in range(diff):
                    self.audio_q.pop(0)
                self.predict(self.audio_q)
            elif len(self.audio_q) == 21:
                self.predict(self.audio_q)
            time.sleep(0.05)

    def run(self, action):
        self.listener.run(self.audio_q)
        self.inference_loop(action)



wakeword_engine = WakeWordEngine('')
action = lambda x: print(x)

wakeword_engine.run(action)
threading.Event().wait()