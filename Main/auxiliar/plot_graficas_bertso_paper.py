from Main import NumberFramesPercentage
from Main import NotePercentage
import numpy as np
import matplotlib.pyplot as plt

#Este script sirve para crear las gráficas de la database de Bertso con los dos parámetros de decisión.
#Aquí se añade también la creación de los 2 vectores con toda la database de los dos parámetros y los labels. 


def main():
    points_counter=0
    spoken=0
    sung=0

    labels_bertso_whole_dataset=[]
    vector_percentages_whole_voiced=[]
    vector_percentages_whole_notes=[]
    for i in range(1,7):
        
        vector_notes_detected=np.loadtxt('Main/Auxiliar/vectors_folder/vector_notes_detected_bertso/vector_notes_detected_b'+str(i)+'.txt')
        f0_cents=np.loadtxt('Main/Auxiliar/vectors_folder/f0_bertso/f0_cents_b'+str(i)+'.txt')
        
        vector_porcentajes_voiced=NumberFramesPercentage.NumberFramesPercentage(f0_cents,window=500)
        vector_porcentajes_notes=NotePercentage.NotePercentage(vector_notes_detected,f0_cents,window=500)
        labels=np.loadtxt('Main/Auxiliar/DATABASE/Labels/speech_and_singing_500ms_window/b'+str(i)+'_labels.txt')

     
        x=[]
        y=[]
        l=[]

        for a in range(len(vector_porcentajes_voiced)):
            if labels[a]!=0:
                x.append(vector_porcentajes_voiced[a])
                y.append(vector_porcentajes_notes[a])
                l.append(labels[a])
                   
        for c in range(100):
            labels_bertso_whole_dataset.append(l[c])
        

        for d in range(100):
            vector_percentages_whole_voiced.append(x[d])

        for e in range(100):
            vector_percentages_whole_notes.append(y[e])
                

        x_spoken=[]
        x_sung=[]
        y_spoken=[]
        y_sung=[]
        

        for b in range(len(x)):
            if l[b]==1:
                x_spoken.append(x[b])
                y_spoken.append(y[b])
            else:
                x_sung.append(x[b])
                y_sung.append(y[b])
        
        


        plt.scatter(x_sung,y_sung,color='orange',alpha=0.5)
        plt.scatter(x_spoken,y_spoken,color='blue',alpha=0.5)
        
        spoken=len(x_spoken)+spoken
        sung=len(x_sung)+sung

        points_counter=points_counter+len(x)



    #np.savetxt('DATABASE/Labels/labels_bertso_training_and_test/labels_bertso_x/labels_whole_bertso.txt',labels_bertso_whole_dataset)
    print(len(vector_percentages_whole_notes),len(vector_percentages_whole_voiced),len(labels_bertso_whole_dataset))
    #np.savetxt('DATABASE/Labels/labels_bertso_training_and_test/labels_bertso_x/vector_porcentajes_voiced_completa.txt',vector_percentages_whole_voiced)
    #np.savetxt('DATABASE/Labels/labels_bertso_training_and_test/labels_bertso_x/vector_porcentajes_notes_completa.txt',vector_percentages_whole_notes)



    
    print(points_counter)
    print(spoken,sung)
    plt.xlabel('PV')
    plt.ylabel('PN')
    plt.legend(loc='upper right')
    plt.show()

    
if __name__=='__main__':

    main()