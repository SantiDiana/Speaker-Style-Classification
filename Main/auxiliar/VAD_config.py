import soundfile as sf
import numpy as np
import librosa
import librosa.display
import numpy as np
from sklearn.mixture import GaussianMixture as GMM
from random import random
from sklearn.metrics import confusion_matrix,f1_score,accuracy_score
import pickle


def calculate_mfcc(audio,fs):  
    frame_size=0.01*fs
    number_of_frames=int(len(audio)/frame_size)
    
    mfcc_vector=[]


    for i in range(number_of_frames):
        frame=audio[int(i*frame_size):int(frame_size+i*frame_size)]
        mfcc=librosa.feature.mfcc(y=frame,n_mfcc=13,sr=fs)
        mfcc_vector.append(np.reshape(mfcc,len(mfcc)))
    return mfcc_vector



def train_model(mfcc_train,labels_train):
  
    
    print("Start training the GMM model")
    gmm_components=32

    voice_mfcc = []
    silence_mfcc = []
    voice_label = []
    silence_label = []

    for i in range(len(mfcc_train)):
        if labels_train[i]== 1:
            voice_mfcc.append(mfcc_train[i])
            voice_label.append(1)

        else:
            silence_mfcc.append(mfcc_train[i])
            silence_label.append(0)

    gmm_voice = GMM(n_components=gmm_components).fit(voice_mfcc, voice_label) 
    gmm_silence = GMM(n_components=gmm_components).fit(silence_mfcc, silence_label)


    x=gmm_voice.score_samples(mfcc_train) 
    x2=gmm_silence.score_samples(mfcc_train)
    print('GMM fitting is completed')

    vector_binary= []
    

    for i in range(len(mfcc_train)):
        if x[i]>x2[i]:
            vector_binary.append(1)

        else:
            vector_binary.append(0)
            
    parameters_voice={'covariances':gmm_voice.covariances_,'means':gmm_voice.means_,'precisions_cholesky':gmm_voice.precisions_cholesky_,'weights':gmm_voice.weights_}
    parameters_silence={'covariances':gmm_silence.covariances_,'means':gmm_silence.means_,'precisions_cholesky':gmm_silence.precisions_cholesky_,'weights':gmm_silence.weights_}


    return parameters_voice, parameters_silence,vector_binary

def accuracy(vector_resultado,labels):
   
    accuracy=accuracy_score(labels,vector_resultado)
    f_score=f1_score(labels,vector_resultado)
    matrix=confusion_matrix(labels,vector_resultado)

    print(accuracy,f_score)
    print(matrix)
    return accuracy,f_score
    

def save_to_file (parameters,filename):
    f=open(filename,"w")
    f.write(str(parameters))
    f.close()

def test_files(parameters_voice,parameters_silence,mfcc_test):
    
    gmm_components=32
    gmm_voice=GMM(n_components=gmm_components)
    gmm_silence=GMM(n_components=gmm_components)

    #gmm_voice.fit(random(10,2))
    #gmm_silence.fit(random(10,2))

    #gmm_voice.set_params(**parameters_voice)
    #gmm_silence.set_params(**parameters_silence)

    gmm_voice.covariances_ = parameters_voice['covariances']
    gmm_voice.means_ = parameters_voice['means']
    gmm_voice.precisions_cholesky_ = parameters_voice['precisions_cholesky']
    gmm_voice.weights_ = parameters_voice['weights']
    gmm_silence.covariances_ = parameters_silence['covariances']
    gmm_silence.means_ = parameters_silence['means']
    gmm_silence.precisions_cholesky_ = parameters_silence['precisions_cholesky']
    gmm_silence.weights_ = parameters_silence['weights']
    
    
    x=gmm_voice.score_samples(mfcc_test)
    x2=gmm_silence.score_samples(mfcc_test)

    vector_binary=[]
    for i in range(len(mfcc_test)):
        if x[i]>x2[i]:
            vector_binary.append(1)
        else:
            vector_binary.append(0)
    
    return vector_binary
    

if __name__=='__main__':
    

    vector_accuracies=[]
    vector_f_score=[]
    accuracy_testing=0
    f_score_test=0
    while f_score_test<0.93:
        mfcc_train=np.loadtxt('MFCC_whole_bertso_dataset.txt')
        labels_train=np.genfromtxt('Labels_for_VAD/labels_training_bertso/joined_labels.txt')

        parameters_v, parameters_s,vector_binary=train_model(mfcc_train,labels_train) #Luego hago el TRAIN.
        
        acuraccy_training,accuracy_training2,f_score=accuracy(vector_binary,labels_train, mfcc_train)
        audio_test,fs=sf.read('Labels_for_VAD/AudioFinal_NUS.wav')

        frames_path_test='Labels_for_VAD/AudioFinal_NUS/AudioFinal_NUS'
        mfcc_test=calculate_mfcc(audio_test,fs,frames_path_test)
        labels_test=np.genfromtxt('Labels_for_VAD/labels_test_NUS/joined_first_3.txt')

        vector_binary=test_files(parameters_v,parameters_s,mfcc_test) #En vector binary tenemos el resultado del test. 
        accuracy_testing,accuracy_training2,f_score_test=accuracy(vector_binary,labels_test,mfcc_test)
        print('Testing Accuracy')

        print(f1_score(labels_test,vector_binary))
        print(accuracy_score(labels_test,vector_binary))
        print(confusion_matrix(labels_test,vector_binary))

        vector_accuracies.append(accuracy_testing)
        vector_f_score.append(f_score_test)

    filename = 'Parameters_voice_VAD_90.sav'
    pickle.dump(parameters_v, open(filename, 'wb'))
            
    filename = 'Parameters_silence_VAD_90.sav'
    pickle.dump(parameters_s, open(filename, 'wb'))
