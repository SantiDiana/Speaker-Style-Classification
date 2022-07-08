from tkinter import Tk,Label,Button,messagebox
from tkinter.filedialog import askopenfilename

from matplotlib.figure import Figure
from main import main
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class window_example:
    def __init__(self,window):
        self.window=window
        self.window.title('Graphic interface')
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.labeltitulo=Label(window, text='Welcome to the Speech and Singing Voice Classifier',font=['Helvetica',20])
        self.labeltitulo.grid(row=0,column=1,pady=20)

        self.button1=Button(window,command=self.openFile,text='Open wav file',width=15,height=3)
        self.button1.grid(row=1,column=1,pady=20)

        self.button2=Button(window,command=self.start_analyzing,text='Start Analyzing',width=15,height=3)
        self.button2.grid(row=2,column=0,pady=20)

        self.labelexp=Label(window, text='0: silence, 1: spoken, 2: sung',font=['Helvetica',20])
        self.labelexp.grid(row=2,column=1,pady=20)
        
        self.path=''
        self.vector=[]
        self.decision_vector=[]
        self.audio=[]
        self.button3=Button(window,command=self.plot,text='See chart',width=15,height=3)
        self.button3.grid(row=2,column=2,pady=20)
        

    def openFile(self):
        file=askopenfilename(title='abrir',filetypes=[('Wav files','*.wav')])  #Esto devuelve la ruta del archivo que seleccionamos, esto se puede meter ahí y ejecutar el audio. 
        if len(file)!=0:  
            ruta=Label(window,text='Audio already selected. You can start analyzing',font=['Helvetica',15])
            ruta.grid(row=3,column=1,pady=20)
            self.path=file

    def start_analyzing(self):
        if self.path=='':
            messagebox.showinfo('Error','First you must select an audio file')
        else:
            self.decision_vector,self.audio=main(self.path)
            print(self.decision_vector)
        
        
    def plot(self):

        self.vector=range(0,len(self.decision_vector))
        # fig,ax=plt.subplots()
        fig=plt.figure(figsize=(3,3))
        plt.plot(self.vector,self.decision_vector,label='Decision')
        plt.plot(self.vector,self.audio,label='Audio')
        plt.legend(loc='upper right')
        
        canvas=FigureCanvasTkAgg(fig,window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4,column=1)
  
    def on_closing(self):
        plt.close()
        self.window.destroy()

    def window_size(self):
        height = self.window.winfo_height()
        width = self.window.winfo_width()
        print(height,width)


window=Tk()
window.geometry('1200x800')
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
myWindow=window_example(window)
myWindow.window_size()
window.mainloop()
