import numpy as np
import matplotlib.pyplot as plt
import NotePercentage
import NumberFramesPercentage


def main(percentage_voiced,percentage_note,f0_cents,n_frames_window,threshold_percentage_notes,threshold_percentage_voiced):

    #0 means silence.
    #1 means speech.
    #2 means singing voice.
    
    

    decision_vector=np.zeros(len(percentage_voiced))

    for i in range(n_frames_window,len(decision_vector)):
        if f0_cents[i]==2500:
            decision_vector[i]=0

    for i in range(n_frames_window,len(decision_vector)):
        for j in range(n_frames_window):
            if f0_cents[i-j]==2500:
                decision_vector[i-j]=0

            elif percentage_note[i]>threshold_percentage_notes and percentage_voiced[i]>threshold_percentage_voiced and f0_cents[i-j]!=2500:
                decision_vector[i-j]=2
            else:
                decision_vector[i-j]=1

    return decision_vector

if __name__=='__main__':
    window=2000
    frame_size=10
    n_frames_window=int(window/frame_size)
    
    c=0
    vector_accuracies=[]
    cont=0
    vector_indices_thresholds=[]

    for i in range(1,14):
        print('Comienzo')
        if i>=1 and i<10:
            f0_cents=np.loadtxt('vectors_folder/f0_spoken/f0_cents_0'+str(i)+'_spoken.txt')
            vector_notes_detected=np.loadtxt('vectors_folder/vector_notes_detected_spoken/vector_notes_detected_0'+str(i)+'_spoken.txt')
        else:
            f0_cents=np.loadtxt('vectors_folder/f0_spoken/f0_cents_'+str(i)+'_spoken.txt')
            vector_notes_detected=np.loadtxt('vectors_folder/vector_notes_detected_spoken/vector_notes_detected_'+str(i)+'_spoken.txt')

        window=1000
        frame_size=10
        n_frames_window=int(window/frame_size)

        percentage_voiced=NumberFramesPercentage.NumberFramesPercentage(f0_cents,window)
        percentage_note=NotePercentage.NotePercentage(vector_notes_detected,f0_cents,window)
        labels=np.loadtxt('DATABASE/Labels/speech/labels_'+str(i)+'spoken.txt')

        for a in range(150,700,50):
            for b in range(150,700,50):
                decision_vector=main(percentage_voiced,percentage_note,f0_cents,n_frames_window,a,b)
                cont=cont+1

                for x in range(len(decision_vector)):
                    if decision_vector[x]==labels[x]:
                        c=c+1

                accuracy_total=c/len(decision_vector)
                vector_accuracies.append(accuracy_total)
                c=0

                if i==1:
                    tupla=a,b
                    vector_indices_thresholds.append(tupla)
                    print(vector_indices_thresholds)
        
        np.savetxt('accuracies_NUS/accuracies_spoken/vector'+str(i),vector_accuracies)
        leng=len(vector_accuracies)
        vector_accuracies=[]
        print('Pasamos al siguiente')

    
        
    vector_suma_accuracies=[0]*121
    print(len(vector_indices_thresholds))

    for i in range(1,14):

        vector=np.loadtxt('accuracies_NUS/accuracies_spoken/vector'+str(i))

        for j in range(len(vector)):
            vector_suma_accuracies[j]=vector_suma_accuracies[j]+vector[j]


    #Recorrer el vector y sacar sus "varios" máximos y sus indices de threshold.
    vector_maximos=[]
    indice_thresholds=[]

    for i in range(70):
        maximo=max(vector_suma_accuracies)
        vector_maximos.append(maximo/13)
        indice=vector_suma_accuracies.index(maximo)
        vector_suma_accuracies[indice]=0
        indice_thresholds.append(vector_indices_thresholds[indice])

    
    print(indice_thresholds)
    np.savetxt('accuracies_NUS/better_thresholds_spoken.txt',indice_thresholds)
    print(vector_maximos)
    np.savetxt('accuracies_NUS/better_acuraccies_spoken.txt',vector_maximos)    
    


