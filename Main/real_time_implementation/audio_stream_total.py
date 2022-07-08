import sounddevice as sd
import pickle
from main_rt import main
import numpy as np


fs=48000
sd.default.samplerate=fs

status=True
c_hablado=0
c_silencio=0
c_cantado=0
c=0
filename = 'Main/Parameters_voice_VAD.sav'
parameters_v= pickle.load(open(filename, 'rb'))

filename2 = 'Main/Parameters_silence_VAD.sav'
parameters_s= pickle.load(open(filename2, 'rb'))

def callback(indata,outdata,time,status,frames=int(fs/5)): #indata: input buffer. outdata: output buffer. 
    global c_hablado,c_silencio,c_cantado,c

    outdata[:] = indata
    vector=audio_processing(indata)
    print(vector)

    for i in range(len(vector)):
        if vector[i]=='1':
            c_hablado=c_hablado+1
        elif vector[i]=='0':
            c_silencio=c_silencio+1
        else:
            c_cantado=c_cantado+1

    if c_hablado>c_silencio and c_hablado>c_cantado:
        print('Talking')
    elif c_cantado>c_silencio and c_cantado>c_hablado:
        print('Singing')
    else:
        print('Silence')
    c_hablado=0
    c_silencio=0
    c_cantado=0
    c=c+1

def audio_processing(audio):
    decision=main(audio,fs,parameters_v,parameters_s)

    return decision
  

        
stream = sd.Stream(blocksize=int(fs/5),callback=callback,channels=1)

with stream:
    input()
    
    