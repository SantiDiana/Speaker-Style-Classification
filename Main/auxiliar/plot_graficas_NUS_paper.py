#Este módulo nos ha servido para calcular los labels y los vectores de los 2 parámetros solo teniendo en cuenta 
#los voiced segments de cara a entrenar el Voice Activity Detector. 

from Main import NumberFramesPercentage
from Main import NotePercentage
import numpy as np
import matplotlib.pyplot as plt


def main():
    points_counter=0
    total_counter=0
    labels_bertso_whole_dataset=[]
    vector_percentages_whole_voiced=[]
    vector_percentages_whole_notes=[]
    f0_cents_complete=[]
    for i in range(1,14):
        if i<10:
            vector_notes_detected=np.loadtxt('Main/Auxiliar/vectors_folder/vector_notes_detected_sung/vector_notes_detected_0'+str(i)+'_sung.txt')
            f0_cents=np.loadtxt('Main/Auxiliar/vectors_folder/f0_sung/f0_cents_0'+str(i)+'_sung.txt')
        else:
            vector_notes_detected=np.loadtxt('Main/Auxiliar/vectors_folder/vector_notes_detected_sung/vector_notes_detected_'+str(i)+'_sung.txt')
            f0_cents=np.loadtxt('Main/Auxiliar/vectors_folder/f0_sung/f0_cents_'+str(i)+'_sung.txt')

        vector_porcentajes_voiced=NumberFramesPercentage.NumberFramesPercentage(f0_cents,window=500)
        vector_porcentajes_notes=NotePercentage.NotePercentage(vector_notes_detected,f0_cents,window=500)
        labels=np.loadtxt('Main/Auxiliar/DATABASE/Labels/singing_500ms_window/labels_'+str(i)+'sung.txt')

        for f in range(len(labels)):
            f0_cents_complete.append(f0_cents[f])
        
        x=[]
        y=[]
        l=[]

        for a in range(len(vector_porcentajes_voiced)):
            if labels[a]!=0:
                x.append(vector_porcentajes_voiced[a])
                y.append(vector_porcentajes_notes[a])
                l.append(labels[a])
                
        if i<10:
            vector_notes_detected2=np.loadtxt('Main/Auxiliar/vectors_folder/vector_notes_detected_spoken/vector_notes_detected_0'+str(i)+'_spoken.txt')
            f0_cents2=np.loadtxt('Main/Auxiliar/vectors_folder/f0_spoken/f0_cents_0'+str(i)+'_spoken.txt')
        else:
            vector_notes_detected2=np.loadtxt('Main/Auxiliar/vectors_folder/vector_notes_detected_spoken/vector_notes_detected_'+str(i)+'_spoken.txt')
            f0_cents2=np.loadtxt('Main/Auxiliar/vectors_folder/f0_spoken/f0_cents_'+str(i)+'_spoken.txt')

        for c in range(len(labels)):
            labels_bertso_whole_dataset.append(labels[c])
        
        for d in range(len(labels)):
            vector_percentages_whole_voiced.append(vector_porcentajes_voiced[d])

        for e in range(len(labels)):
            vector_percentages_whole_notes.append(vector_porcentajes_notes[e])

        

        vector_porcentajes_voiced2=NumberFramesPercentage.NumberFramesPercentage(f0_cents2,window=500)
        vector_porcentajes_notes2=NotePercentage.NotePercentage(vector_notes_detected2,f0_cents2,window=500)
        labels2=np.loadtxt('Main/Auxiliar/DATABASE/Labels/speech_500ms_window/labels_'+str(i)+'spoken.txt')

        x2=[]
        y2=[]
        l2=[]
    
        for b in range(len(vector_porcentajes_voiced2)):
            if labels2[b]!=0:
                x2.append(vector_porcentajes_voiced2[b])
                y2.append(vector_porcentajes_notes2[b])
                l2.append(labels2[b])

        for c in range(len(labels2)):
            labels_bertso_whole_dataset.append(labels2[c])
        
        for d in range(len(labels2)):
            vector_percentages_whole_voiced.append(vector_porcentajes_voiced2[d])

        for e in range(len(labels2)):
            vector_percentages_whole_notes.append(vector_porcentajes_notes2[e])
            
        for f in range(len(labels2)):
            f0_cents_complete.append(f0_cents2[f])

        plt.scatter(x,y,color='orange',alpha=0.5)
        plt.scatter(x2,y2,color='blue',alpha=0.5)
        
        total_counter=total_counter+len(vector_porcentajes_notes)+len(vector_porcentajes_notes2)
        points_counter=points_counter+len(x)+len(x2)

    #np.savetxt('DATABASE/Labels/labels_NUS_training_and_test/labels_whole_NUS_with_silence.txt',labels_bertso_whole_dataset)
    #np.savetxt('DATABASE/Labels/labels_NUS_training_and_test/vector_porcentajes_voiced_completa_with_silence.txt',vector_percentages_whole_voiced)
    #np.savetxt('DATABASE/Labels/labels_NUS_training_and_test/vector_porcentajes_notes_completa_with_silence.txt',vector_percentages_whole_notes)
    #np.savetxt('DATABASE/Labels/labels_NUS_training_and_test/f0_cents_complete_with_silence.txt',f0_cents_complete)

    plt.xlabel('PV')
    plt.ylabel('PN')
    plt.legend(loc='upper right')
    plt.show()

    
if __name__=='__main__':
    main()