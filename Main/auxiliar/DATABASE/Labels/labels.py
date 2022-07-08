import numpy as np



labels_frame=np.loadtxt('DATABASE/Labels/speech_and_singing/b6_labels.txt')

labels=[]
cont_unos=0
cont_doses=0
for i in range(0,29500,50):
    for j in range(50):
            if labels_frame[i+j]==1:
                cont_unos=cont_unos+1
            if labels_frame[i+j]==2:
                cont_doses=cont_doses+1
        
    if cont_unos==0 and cont_doses==0:
        labels.append(0)
    elif cont_unos!=0 and cont_doses==0:
        labels.append(1)
    elif cont_unos==0 and cont_doses!=0:
        labels.append(2)
    elif cont_unos!=0 and cont_doses!=0:
        if cont_unos>cont_doses:
            labels.append(1)
        else:
            labels.append(2)
        
       
    cont_unos=0
    cont_doses=0

np.savetxt('DATABASE/Labels/speech_and_singing_500ms_window/b6_labels.txt',labels)
