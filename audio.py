import pyaudio
import wave
import thread

def input_thread(list):
    raw_input()
    list.append(None)

def record():
    list = []
    thread.start_new_thread(input_thread, (list,))
    while not list:
        data = stream.read(CHUNK)
        frames.append(data)
        

CHUNK = 1024 
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2 
RATE = 44100 #sample rate
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "sounds/output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

print("* recording")

frames = []

record()

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

"""
def read_frames_from_mic(nframes):
    CHUNK = 1024 
    FORMAT = pyaudio.paInt16 #paInt8
    CHANNELS = 1 
    RATE = 44100 #sample rate
    #WAVE_OUTPUT_FILENAME = "sounds/output.wav"
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
    
    res =  stream.read(nframes)
    stream.close()
    return res
import numpy as np

    
print np.fromstring(read_frames_from_mic(100), 'Int16')
"""