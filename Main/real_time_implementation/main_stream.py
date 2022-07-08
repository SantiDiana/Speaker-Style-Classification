from msilib.schema import SelfReg
import sounddevice as sd
import pickle
from main_rt import main
import numpy as np
from tkinter import Tk,Label,Button,messagebox

class window_example:
    def __init__(self,window):
        self.window=window
        self.window.title('Real time GUI')
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.labeltitulo=Label(window, text='Welcome to the real-time Speech and Singing Voice Classifier',font=['Helvetica',20])
        self.labeltitulo.grid(row=0,column=1,pady=50)

        self.labelexp=Label(window, text='Press the "analyze" button to start analyzing',font=['Helvetica',15])
        self.labelexp.grid(row=1,column=1,pady=20)

        self.button1=Button(window,command=self.start_analyzing,text='Start Analyzing',width=15,height=3)
        self.button1.grid(row=2,column=0,pady=20)

        self.button2=Button(window,command=self.on_closing,text='Stop Analyzing',width=15,height=3)
        self.button2.grid(row=2,column=2,pady=20)

        self.labelstate=Label(window, text='',font=['Helvetica',20])
        self.labelstate.grid(row=3,column=1,pady=20)
        self.fs=48000

        self.filename = 'Main/Parameters_voice_VAD.sav'
        self.parameters_v= pickle.load(open(self.filename, 'rb'))

        self.filename2 = 'Main/Parameters_silence_VAD.sav'
        self.parameters_s= pickle.load(open(self.filename2, 'rb'))



    def start_analyzing(self):
        fs=48000
        sd.default.samplerate=fs
        self.stream()

        


    def callback(self,indata,time,status,frames=int(48000/5)): #indata: input buffer. outdata: output buffer. 
        global c_hablado,c_silencio,c_cantado,c

        c_hablado=0
        c_silencio=0
        c_cantado=0
        c=0
       
        print(indata)
        vector=self.audio_processing(indata)
        print(vector)

        for i in range(len(vector)):
            if vector[i]=='1':
                c_hablado=c_hablado+1
            elif vector[i]=='0':
                c_silencio=c_silencio+1
            else:
                c_cantado=c_cantado+1

        if c_hablado>c_silencio and c_hablado>c_cantado:
            self.labelstate=Label(window, text='Talking',font=['Helvetica',20])
            self.labelstate.grid(row=3,column=1,pady=20)
        elif c_cantado>c_silencio and c_cantado>c_hablado:
            self.labelstate=Label(window, text='Singing',font=['Helvetica',20])
            self.labelstate.grid(row=3,column=1,pady=20)
        else:
            self.labelstate=Label(window, text='Silence',font=['Helvetica',20])
            self.labelstate.grid(row=3,column=1,pady=20)
        c_hablado=0
        c_silencio=0
        c_cantado=0
        c=c+1

    def audio_processing(self,audio):
        decision=main(audio,self.fs,self.parameters_v,self.parameters_s)

        return decision
    
    def stream(self):
        self.audiostream = sd.InputStream(blocksize=int(48000/5),callback=self.callback,channels=1)
        print('Escuchando')

        with self.audiostream:
            input()

    def on_closing(self):
        self.audiostream.stop()
        self.window.destroy()

window=Tk()
window.geometry('1200x800')
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
myWindow=window_example(window)
window.mainloop()

        




