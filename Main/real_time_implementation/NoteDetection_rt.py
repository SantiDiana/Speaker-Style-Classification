import numpy as np
import matplotlib.pyplot as plt
import math

def NoteDetection(f0_cents,vector_binary):

    #Si entra al Note Detection Algorithm es porque cumple las condiciones, si no sigue hacia adelante. 
    #Más virguerías, para el máximo y mínimo no debería utilizar los dos primeros que suelen tener una mala confidence. 

    vector_notes_detected=np.zeros(len(f0_cents))

    f0_cents_altered=[]
    for i in range(len(f0_cents)): #Aquí implemento que no tenga en cuenta los ceros para el cálculo del máximo y el mínimo. 
        if f0_cents[i]!=2500:
            f0_cents_altered.append(f0_cents[i])




    maximum=max(f0_cents_altered[3:len(f0_cents_altered)])
    minimum=min(f0_cents_altered[3:len(f0_cents_altered)])

    print('maximos')
    print(maximum,minimum)
    if maximum-minimum<100:
        for j in range(len(f0_cents)):
            if vector_binary[j]=='Talking':
                vector_notes_detected[j]=1000
            else:
                vector_notes_detected[j]=0
    else:
        for x in range(len(f0_cents)):
            vector_notes_detected[x]=0
    
    return vector_notes_detected
    
    
        
    


    

   

