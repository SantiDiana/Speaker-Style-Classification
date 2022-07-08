import numpy as np
import VAD
import pickle
import soundfile as sf
from sklearn.metrics import confusion_matrix,recall_score,precision_score

audio_test,fs=sf.read('Main/Auxiliar/DATABASE/whole_NUS_audio.wav')
labels_test=np.loadtxt('Main/Auxiliar/Labels_for_VAD/labels_test_NUS/joined_labels_rounded.txt') #Creo que esto es sung1...sung13 y luego spoken1...spoken13.
filename = 'Parameters_voice_VAD_90.sav'
parameters_v= pickle.load(open(filename, 'rb'))
filename = 'Parameters_silence_VAD_90.sav'
parameters_s= pickle.load(open(filename, 'rb'))


mfcc_test=VAD.calculate_mfcc(audio_test,fs)
vector_binary_test=VAD.test_files(parameters_v,parameters_s,mfcc_test)
print('Accuracy and f-score')
accuracy_test=VAD.accuracy(vector_binary_test,labels_test)

print(confusion_matrix(labels_test,vector_binary_test))
print('Recall: '+str(recall_score(labels_test,vector_binary_test)))
print('Precision: '+str(precision_score(labels_test,vector_binary_test)))


#Accuracy de 89.96% y f-score de 93.26%. 

# Accuracy and f-score
# 0.8996146090073941 0.9326056674900042
# [[ 45756   6967]
#  [ 15434 154993]]
# Recall: 0.9094392320465654
# Precision: 0.9569832057298099

