import numpy as np
from Main import SVM
from sklearn.metrics import confusion_matrix, f1_score


 
labels_500ms=np.loadtxt('Main/auxiliar/DATABASE/Labels/labels_NUS_training_and_test/labels_whole_NUS_with_silence.txt') 
labels_frame=np.loadtxt('Main/auxiliar/DATABASE/Labels/labels_NUS_training_and_test/labels_complete_with_silence.txt')
f0_cents=np.loadtxt('Main/auxiliar/DATABASE/Labels/labels_NUS_training_and_test/f0_cents_complete_with_silence.txt')
prediction_vector=SVM.SVM_test()

c=0
labels_500ms_prediction=np.zeros(len(labels_500ms))  #Este vector es el vector que ya ha sido predecido pero en ventanas de 500ms, ahora falta pasarlo a nivel de frame. 
#Diríamos que es 

for i in range(len(labels_500ms)):
    if labels_500ms[i]==0:  #Es trampa esta parte? Claro, como solo he pasado por el test los que están etiquetados como 1 o 2... Hay errores que no he pasado por ahí?
        labels_500ms_prediction[i]=0
    else:
        labels_500ms_prediction[i]=prediction_vector[c]
        c=c+1

 
vector_final_decision=np.zeros(len(f0_cents))  #Este vector es un vector a nivel de frame, que en el caso de NUS SUNG tiene 223150 muestras o algo así. 

for i in range(len(labels_500ms_prediction)):
    for j in range(i*50,i*50+50):
        
        if labels_500ms_prediction[i]==0: #Si el label es 0, significa que no ha pasado por el clasificador, por lo tanto se queda igual que como estaba.
            vector_final_decision[j]=0
        if labels_500ms_prediction[i]==1:
            if f0_cents[j]==2500:
                vector_final_decision[j]=0
            else:
                vector_final_decision[j]=1
        if labels_500ms_prediction[i]==2:
            if f0_cents[j]==2500:
                vector_final_decision[j]=0
            else:
                vector_final_decision[j]=2

            
acierto=0
for i in range(len(vector_final_decision)):
    if labels_frame[i]==vector_final_decision[i]:
        acierto=acierto+1

print(acierto)    
print('F-score media con weights de todo el algoritmo con NUS Sung como test '+str(f1_score(labels_frame,vector_final_decision,average='weighted')))
print('F-score por clases: [Silencio, Hablado, Cantado]: '+str(f1_score(labels_frame,vector_final_decision,average=None)))
print(confusion_matrix(labels_frame,vector_final_decision)) 





    
