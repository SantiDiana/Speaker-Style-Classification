import sounddevice as sd
import pickle
import VAD_rt
import numpy as np


fs=48000
sd.default.samplerate=fs

c=0
status=True
c_hablado=0
c_silencio=0
filename = 'Main/Parameters_voice_VAD.sav'
parameters_v= pickle.load(open(filename, 'rb'))

filename = 'Main/Parameters_silence_VAD.sav'
parameters_s= pickle.load(open(filename, 'rb'))

def callback(indata,outdata,time,status,frames=int(fs/5)): #indata: input buffer. outdata: output buffer. 
    global c
    global c_hablado
    global c_silencio

    outdata[:] = indata
    vector=audio_processing(indata)

    for i in range(len(vector)):
        if vector[i]=='Talking':
            c_hablado=c_hablado+1
        else:
            c_silencio=c_silencio+1

    if c_hablado>c_silencio:
        print('Talking')
    else:
        print('Silencio')
    c_hablado=0
    c_silencio=0

    

def audio_processing(buffer_to_analyze):
    
    mfcc_test=VAD_rt.calculate_mfcc(buffer_to_analyze,fs) #MFCC calculation frame by frame. 
    vector_binary_test=VAD_rt.test_files(parameters_v,parameters_s,mfcc_test)

    return vector_binary_test

        
stream = sd.Stream(blocksize=int(fs/5),callback=callback,channels=1)

with stream:
    input()
    # duration=10
    # recording=sd.rec(int(duration*fs),samplerate=fs,channels=1)
    # print('GRABANDO')
    
    
    
