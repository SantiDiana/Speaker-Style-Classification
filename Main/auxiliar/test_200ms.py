import numpy as np
from Main import SVM2
from sklearn.metrics import confusion_matrix, f1_score


 
labels_200ms=np.loadtxt('Main/auxiliar/DATABASE/Labels/labels_200ms/NUS/labels_200ms_with_silence.txt') 
labels_frame=np.loadtxt('Main/auxiliar/DATABASE/Labels/labels_200ms/whole_NUS.txt')
f0_cents=np.loadtxt('Main/auxiliar/DATABASE/Labels/labels_200ms/whole_NUS_f0_cents.txt')

SVM2.SVM_training()
prediction_vector=SVM2.SVM_test()

c=0
labels_200ms_prediction=np.zeros(len(labels_200ms))  

for i in range(len(labels_200ms)):
    if labels_200ms[i]==0:  
        labels_200ms_prediction[i]=0
    else:
        labels_200ms_prediction[i]=prediction_vector[c]
        c=c+1

 
vector_final_decision=np.zeros(len(f0_cents)) 

for i in range(len(labels_200ms_prediction)):
    for j in range(i*20,i*20+20):
        
        if labels_200ms_prediction[i]==0: 
            vector_final_decision[j]=0
        if labels_200ms_prediction[i]==1:
            if f0_cents[j]==2500:
                vector_final_decision[j]=0
            else:
                vector_final_decision[j]=1
        if labels_200ms_prediction[i]==2:
            if f0_cents[j]==2500:
                vector_final_decision[j]=0
            else:
                vector_final_decision[j]=2

            
success=0
for i in range(len(vector_final_decision)):
    if labels_frame[i]==vector_final_decision[i]:
        success=success+1

print(success)    
print('Mean F-score with weights of the entire algorithm with NUS Sung as test '+str(f1_score(labels_frame,vector_final_decision,average='weighted')))
print('F-score by classes: [Silent, Spoken, Sung]: '+str(f1_score(labels_frame,vector_final_decision,average=None)))
print(confusion_matrix(labels_frame,vector_final_decision)) 






# matrix=np.zeros((3,3))


# c1=0
# c2=0
# c3=0
# c4=0
# c5=0
# c6=0
# c7=0
# c8=0
# c9=0

# for i in range(len(labels_frame)):
#     if labels_frame[i]==0 and vector_final_decision[i]==0:
#         c1=c1+1
#     elif  labels_frame[i]==1 and vector_final_decision[i]==0:
#         c2=c2+1
#     elif  labels_frame[i]==2 and vector_final_decision[i]==0:
#         c3=c3+1
#     elif  labels_frame[i]==0 and vector_final_decision[i]==1:
#         c4=c4+1
#     elif  labels_frame[i]==1 and vector_final_decision[i]==1:
#         c5=c5+1
#     elif  labels_frame[i]==2 and vector_final_decision[i]==1:
#         c6=c6+1
#     elif  labels_frame[i]==0 and vector_final_decision[i]==2:
#         c7=c7+1
#     elif labels_frame[i]==1 and vector_final_decision[i]==2:
#         c8=c8+1
#     elif  labels_frame[i]==2 and vector_final_decision[i]==2:
#         c9=c9+1

#     matrix[0][0]=c1 
#     matrix[0][1]=c2 
#     matrix[0][2]=c3 
#     matrix[1][0]=c4 
#     matrix[1][1]=c5 
#     matrix[1][2]=c6 
#     matrix[2][0]=c7 
#     matrix[2][1]=c8 
#     matrix[2][2]=c9 

# print(matrix)
       





    


#La dinámica debería ser, una vez tenemos la señal de f0_cents, le hacemos el note detection,
#donde los segmentos menores de 150ms ni siquiera son analizados. Una vez eso hecho, calculamos
#el note percentage y number of frames percentage, pasándole la ventana de 500ms. Es probable que si hay muchos fallos puntuales de la f0, del VAD... pocos segmentos tengan 
#los 2 parámetros a 0, en cuyo caso serían catalogados directamente como silencio y no pasarían por el clasificador. (Deberíamos incluir una mejora que fuera quitarnos los segmentos voiced
# que son muy cortos, porque de esta manera quitaríamos bastantes errores puntuales). Una vez eso, pasamos por el clasificador solo los segmentos donde la dupla PV,PN!=0,0. Hacemos la clasificación,
# y los que deberían ser silencios pero son errores me da igual como me los catalogue, siguen siendo errores. 

#Esto se debería hacer todo en la MAIN function, esta función de test es SOLO para el NUS Sung, para el análisis total. Para un segmento cualquiera deberíamos hacerlo fuera de aquí. 






#NADA ORGULLOSO DE ESTA PEDAZO DE MIERDA, PERO QUIERO OBSERVAR CUANTOS CEROS SE DIBUJAN BIEN Y TAL. 

# for i in range(1,14):
#     if i<10:
#         vector_notes_detected=np.loadtxt('vectors_folder/vector_notes_detected_sung/vector_notes_detected_0'+str(i)+'_sung.txt')
#         f0_cents=np.loadtxt('vectors_folder/f0_sung/f0_cents_0'+str(i)+'_sung.txt')
#         labels=np.loadtxt('DATABASE/Labels/singing/labels_'+str(i)+'sung.txt')
#     else:
#         vector_notes_detected=np.loadtxt('vectors_folder/vector_notes_detected_sung/vector_notes_detected_'+str(i)+'_sung.txt')
#         f0_cents=np.loadtxt('vectors_folder/f0_sung/f0_cents_'+str(i)+'_sung.txt')
#         labels=np.loadtxt('DATABASE/Labels/singing/labels_'+str(i)+'sung.txt')


#     longitud=len(labels)
#     a = [int(a) for a in str(longitud)]
#     print(a)
#     print(a[len(a)-1])
#     if a[len(a)-2]>=5:
#         a[len(a)-2]=5
#         a[len(a)-1]=0
#     else:
#         a[len(a)-2]=0
#         a[len(a)-1]=0

#     longitud=str(a[0])
#     for b in range(1,len(a)):
#         longitud=longitud+str(a[b])
    
#     longitud=int(longitud)


#     for z in range(longitud):
#         labels_frame.append(labels[z])

    


#     if i<10:
#         vector_notes_detected2=np.loadtxt('vectors_folder/vector_notes_detected_spoken/vector_notes_detected_0'+str(i)+'_spoken.txt')
#         f0_cents2=np.loadtxt('vectors_folder/f0_spoken/f0_cents_0'+str(i)+'_spoken.txt')
#         labels2=np.loadtxt('DATABASE/Labels/speech/labels_'+str(i)+'spoken.txt')
#     else:
#         vector_notes_detected2=np.loadtxt('vectors_folder/vector_notes_detected_spoken/vector_notes_detected_'+str(i)+'_spoken.txt')
#         f0_cents2=np.loadtxt('vectors_folder/f0_spoken/f0_cents_'+str(i)+'_spoken.txt')
#         labels2=np.loadtxt('DATABASE/Labels/speech/labels_'+str(i)+'spoken.txt')


#     longitud=len(labels2)
#     a = [int(a) for a in str(longitud)]
#     print(a)
#     print(a[len(a)-1])
#     if a[len(a)-2]>=5:
#         a[len(a)-2]=5
#         a[len(a)-1]=0
#     else:
#         a[len(a)-2]=0
#         a[len(a)-1]=0

#     longitud=str(a[0])
#     for b in range(1,len(a)):
#         longitud=longitud+str(a[b])
    
#     longitud=int(longitud)


#     for z in range(longitud):
#         labels_frame.append(labels2[z])

    



