import pyaudio
import wave
import thread
import numpy as np
def input_thread(list):
    raw_input()
    list.append(None)

        
"""
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
def read_frames_from_mic(nframes, rate):
    FORMAT = pyaudio.paInt16 #paInt8
    CHANNELS = 1 
    CHUNK = 1024
    #WAVE_OUTPUT_FILENAME = "sounds/output.wav"
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=rate,
                input=True,
                frames_per_buffer=CHUNK)
    
    res =  stream.read(nframes)
    stream.close()
    return res

#Records from default recording device for time_ms
def record_for_time(time_ms):
	rate = 44100 #sampling rates in hertz

	frames = time_ms * rate // 1000
	#the raw bytes for the data stream
	return read_frames_from_mic(frames, rate)

#records for a specified time and converts the spectral reading for that interval
def read_spectral_data_for_time(time_ms):
	raw_data = record_for_time(time_ms)
	t = np.fromstring(raw_data, 'Int16')
	freq_sig = np.abs(np.fft.fft(t))
	return freq_sig
if __name__ == '__main__':
	print read_spectral_data_for_time(500)
