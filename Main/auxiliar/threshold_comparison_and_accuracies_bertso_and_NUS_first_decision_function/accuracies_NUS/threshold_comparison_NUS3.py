#EJECUTANDO ESTE FICHERO, TENEMOS LA MÁXIMA ACCURACY EN FUNCIÓN DE LOS THRESHOLD EN TODA LA NUS SUNG DATABASE. Repasar a ver si nos hemos dejado algo.

#Aquí hemos hecho la media de accuracies para cada threshold de todos los audios, tanto cantados como hablados, y luego hemos sumado y dividido entre 2 las accuracies correspondientes a cada combinación de thresholds. 

import numpy as np


accuracies_spoken=np.loadtxt('accuracies_NUS/vector_suma_accuracies_spoken.txt')
accuracies_sung=np.loadtxt('accuracies_NUS/vector_suma_accuracies_sung.txt')
vector_indices=np.loadtxt('accuracies_NUS/vector_indices_thresholds.txt')

print(len(accuracies_spoken))


accuracy_total=[0]*121
for i in range(len(accuracies_spoken)):
    accuracy_total[i]=(accuracies_spoken[i]+accuracies_sung[i])/26


print(accuracy_total)
print(max(accuracy_total))
print(accuracy_total.index(max(accuracy_total)))
print(vector_indices[accuracy_total.index(max(accuracy_total))]) 


