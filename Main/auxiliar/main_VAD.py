#This is the main script for the project. Here will be placed the execution of the whole algorithm, starting in VAD detection, f0 estimation, note detection and finally decision making. 

import VAD
import evaluate_pitch2
import NoteDetection
import NotePercentage
import NumberFramesPercentage2
import SVM
import soundfile as sf
#import frames_creator
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score,confusion_matrix


import scipy.io.wavfile as wavf



#PASAR A MONO. 
def main():
    audio_test,fs=sf.read('audio/whole_NUS_audio.wav')
   
    #The VAD was already trained, so now we come up with the parameters already trained of the VAD. We import them. 
    filename = 'Parameters_voice_VAD_90.sav'
    parameters_v= pickle.load(open(filename, 'rb'))

    filename = 'Parameters_silence_VAD_90.sav'
    parameters_s= pickle.load(open(filename, 'rb'))
    print('Empiezo a calcular los MFCC del test')
    mfcc_test=VAD.calculate_mfcc(audio_test,fs)
    print('Comienza el test del VAD. Pasamos el audio por el VAD')
    vector_binary_test=VAD.test_files(parameters_v,parameters_s,mfcc_test)
    labels_test=np.loadtxt('Labels_for_VAD/labels_test_NUS/joined_labels_rounded.txt')
    np.savetxt('vector_binary.txt',vector_binary_test)
    accuracy_test=VAD.accuracy(vector_binary_test,labels_test)
    # print(confusion_matrix(labels_test,vector_binary_test))
    #Here we already have the vector with the VAD decision done. 1-- voice and 0-- silence. 
    print('El VAD ya ha acabado')

 ############   ############   ############   ############   ############   ############   ############   ############   ############   ############   ############
    
    #F0 detection algorithm. Solo son calculadas las f0 de las cosas que nos interesan, es decir, que mantienen cierta confidence (de los silencios o ruido probablemente la f0 ni siquiera es calculada).
    f0_curve,confidence=evaluate_pitch2.f0_extraction('audio')
    f0_curve=f0_curve[1:len(f0_curve)]
    confidence=confidence[1:len(confidence)]

    
    f0_curve_treated=evaluate_pitch2.f0_treatment(f0_curve,vector_binary_test)   ##SALIDA DEL F0 aplicado el VAD, es decir, f0[i]!=0 es voiced segment, y tiene x f0. 
    #La curva de f0 está multiplicada tanto por el VAD como por la curva de CONFIDENCE. El VAD nos dejaba pasar algunas cosas que no nos deja la confidence, así que tenemos como 2 barreras para los segmentos que no son de interés (solo nos interesan las f0 de los voiced segments).
    
    #dnn_f0 solo nos calcula las f0 de los segmentos que pasan de 0.6 de confidence y que son determinados por el VAD como voiced segment. Lo demás no se calcula. 
    

 #############    #############    #############    #############    #############    #############    #############    #############    #############    #############    
    #Note Detection Algorithm. Este método devuelve un vector igual de largo que el audio donde 1000 equivale a frame como nota detectada y 0 equivale a frame como nota no detectada. 
    #Ahora habrá que combinar esto con si es voiced frame o no, porque que no sea detectada como nota puede significar o que sea voiced hablado o que sea silencio. 
    #if == voiced pero no es igual a nota, entonces es hablado. Si son las 2 cosas, cantando. Si no es ninguna de las 2 cosas, entonces silencio. Algo así es la lógica.
    
    print('Empieza Note Detection Algorithm')
    vector_notes_detected,f0_cents=NoteDetection.NoteDetection(f0_curve_treated)
    print('Ya ha acabado el Note Detection')
    #Una vez tenemos las notas detectadas y su f0 en cents, procedemos a calcular los porcentajes.


    window=500
    voiced_frame_percentage=NumberFramesPercentage2.NumberFramesPercentage(f0_cents,window)
    notes_percentage=NotePercentage.NotePercentage(vector_notes_detected,f0_cents,window)


    #Ya tenemos los dos vectores, donde quedan los pares de cada 500ms del audio. Tenemos por tanto n_frames/50 elementos en estos 2 vectores.
    #Deberían quedarse fuera del paso por el SVM las windows de 500ms donde no hay detectado NADA de ruido, es decir, donde f0_cents=2500 durante toda la window. 
   
    vector_through_SVM_voiced=[] #Vectores que van a pasar por el SVM. 
    vector_through_SVM_note=[] #Vectores que van a pasar por el SVM. 

    for i in range(len(voiced_frame_percentage)):
        if voiced_frame_percentage[i]!=0 or notes_percentage[i]!=0:  #Debería funcionar si los 2 son cero?
            vector_through_SVM_voiced.append(voiced_frame_percentage[i])
            vector_through_SVM_note.append(notes_percentage[i])


    prediction_vector=SVM.SVM_prediction(vector_through_SVM_voiced,vector_through_SVM_note)  #Aquí tengo el vector de decisión sobre las ventanas que eran diferentes de 0,0. 

    #Ahora toca juntar lo que no ha pasado por el SVM y lo que sí y ya está.

    decision_windowed=np.zeros(len(voiced_frame_percentage))  #Vector de decisión pero por ventanas. 
    c=0
    for i in range(len(voiced_frame_percentage)):
        if  voiced_frame_percentage[i]==0 and notes_percentage[i]==0:
            decision_windowed[i]=0
        else:
            decision_windowed[i]=prediction_vector[c]
            c=c+1

   
    decision_vector=np.zeros(len(f0_cents))  #Vector de decisión final a nivel de frame. 

    for i in range(len(decision_windowed)):
        for j in range(int(i*window/10),int(i*window/10)+int(window/10)):
            if decision_windowed[i]==0:
                    decision_vector[j]=0
            if decision_windowed[i]==1:
                if vector_binary_test[j]==0:  ##Esto está bien porque ya ha pasado por el Voice Activity Detector y por la confidence. 
                    decision_vector[j]=0
                else:
                    decision_vector[j]=1
            if decision_windowed[i]==2:
                if vector_binary_test[j]==0:
                    decision_vector[j]=0
                else:
                    decision_vector[j]=2
            

    return decision_vector
            
            

#Voy a sacar a mano todos los decision vector con las diferentes configuraciones del NUS Sung and spoken, a ver qué comparación de métricas se puede hacer. 
#Hay que conseguir que los últimos frames de la window que no está completa se analicen también. No lo vamos a hacer para la NUS pero en el algoritmo general hay que hacerlo. 


#Si el audio cortado que estoy haciendo está bien se puede ejecutar desde el principio todo y comparar las métricas de los diferentes métodos. 
if __name__=='__main__':
    decision_vector=main()

    labels=np.loadtxt('labels_sung1,sung2.txt')
    
    acierto=0
    for i in range(len(decision_vector)):
        if decision_vector[i]==0 and labels[i]==0:
            acierto=acierto+1
        if decision_vector[i]==2 and labels[i]==2:
            acierto=acierto+1
        if decision_vector[i]==1 and labels[i]==1:
            acierto=acierto+1
            

    print(acierto,len(decision_vector))
    print('Accuracy: '+str(acierto/len(decision_vector)))

    #print(accuracy_score(labels,decision_vector,average='weighted'))
    print('Labels por clases: '+str(f1_score(labels,decision_vector,average=None)))
    print('Esto es la f-score:' +str(f1_score(labels,decision_vector,average='weighted')))
    print(confusion_matrix(labels,decision_vector))