#This is the main script for the project. Here will be placed the execution of the whole algorithm, starting in VAD detection, f0 estimation, note detection and finally decision making. 
import evaluate_pitch
import NoteDetection
import NotePercentage
from Main import NumberFramesPercentage
import SVM
import soundfile as sf
import numpy as np



import scipy.io.wavfile as wavf

#PASAR A MONO. 
def main():
    audio_test,fs=sf.read('audio/13_spoken.wav')
   
    f0_curve,confidence=evaluate_pitch.f0_extraction('audio')
    f0_curve=f0_curve[1:len(f0_curve)]
    confidence=confidence[1:len(confidence)]

    
    f0_curve_treated=evaluate_pitch.f0_treatment(f0_curve,confidence)  #Treatment of the f0_curve by applying the confidence curve.  
   

#############    #############    #############    #############    #############    #############    #############    #############    #############    #############    
    #Note Detection Algorithm. Este método devuelve un vector igual de largo que el audio donde 1000 equivale a frame como nota detectada y 0 equivale a frame como nota no detectada. 
    #Ahora habrá que combinar esto con si es voiced frame o no, porque que no sea detectada como nota puede significar o que sea voiced hablado o que sea silencio. 
    #if == voiced pero no es igual a nota, entonces es hablado. Si son las 2 cosas, cantando. Si no es ninguna de las 2 cosas, entonces silencio. Algo así es la lógica.
    
    print('Empieza Note Detection Algorithm')
    vector_notes_detected,f0_cents=NoteDetection.NoteDetection(f0_curve_treated)
    print('Ya ha acabado el Note Detection')
    #Una vez tenemos las notas detectadas y su f0 en cents, procedemos a calcular los porcentajes.


    window=500
    voiced_frame_percentage=NumberFramesPercentage.NumberFramesPercentage(f0_cents,window)
    notes_percentage=NotePercentage.NotePercentage(vector_notes_detected,f0_cents,window)

    # np.savetxt('prueba/voiced_frame_percentage.txt',voiced_frame_percentage)
    # np.savetxt('prueba/notes_percentage.txt',notes_percentage)

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
                if f0_cents[j]==2500:  ##Esto está bien porque ya ha pasado por el Voice Activity Detector y por la confidence. 
                    decision_vector[j]=0
                else:
                    decision_vector[j]=1
            if decision_windowed[i]==2:
                if f0_cents[j]==2500:
                    decision_vector[j]=0
                else:
                    decision_vector[j]=2
            

    return decision_vector
            
            

#Voy a sacar a mano todos los decision vector con las diferentes configuraciones del NUS Sung and spoken, a ver qué comparación de métricas se puede hacer. 
#Hay que conseguir que los últimos frames de la window que no está completa se analicen también. No lo vamos a hacer para la NUS pero en el algoritmo general hay que hacerlo. 


#Si el audio cortado que estoy haciendo está bien se puede ejecutar desde el principio todo y comparar las métricas de los diferentes métodos. 
if __name__=='__main__':
    decision_vector=main()

    
    
  





#Usando audio_sung_01.

#MÉTRICAS PARA LAS DOS COSAS JUNTAS. 
# 0.8178532138928178
# 0.8589069366530856
# [[7.64e+02 0.00e+00 5.35e+02]
#  [1.00e+00 0.00e+00 5.03e+02]
#  [1.20e+02 0.00e+00 4.44e+03]]


#MÉTRICAS PARA SOLO CONFIDENCE.

# 5442 6363
# 0.8552569542668552
# 0.8947688055125559
# [[ 872.    0.  396.]
#  [   0.    0.  512.]
#  [  13.    0. 4570.]]

#MÉTRICAS PARA SOLO VAD.
# 5094 6363
# 0.8005657708628006
# 0.8445041303292394
# [[7.760e+02 0.000e+00 6.400e+02]
#  [1.000e+00 0.000e+00 5.200e+02]
#  [1.080e+02 0.000e+00 4.318e+03]]




##################################################
# No entiendo qué ha cambiado para que ahora me salgan estas métricas. 
#Con el audio sung1:
# 5504 6350
# Accuracy: 0.8667716535433071
# Labels por clases: [0.80733083 0.         0.91653512]
# Esto es la f-score:0.9015388789544663
# [[ 859    0   13]
#  [   0    0    0]
#  [ 397  436 4645]]





