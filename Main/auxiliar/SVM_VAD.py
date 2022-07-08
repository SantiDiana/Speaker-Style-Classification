import numpy as np
from sklearn import svm
from sklearn.metrics import cohen_kappa_score, f1_score, accuracy_score, recall_score,precision_score,cohen_kappa_score,confusion_matrix
import pickle
import librosa 
import librosa.display
from sklearn.semi_supervised import LabelSpreading


def SVM_VAD_training(mfcc_train,labels_train):
    model=svm.SVC(kernel='linear',class_weight='balanced')
    model.fit(mfcc_train,labels_train)
    print('Model trained')

    filename = 'SVM_VAD_trained.sav'
    pickle.dump(model, open(filename, 'wb'))


def SVM_VAD_test(fs):
    filename = 'SVM_VAD_trained.sav'
    model = pickle.load(open(filename, 'rb'))

    
    mfcc_vector=calculate_mfcc('audio/whole_NUS_audio.wav',fs)
    labels=np.loadtxt('Labels_for_VAD/labels_test_NUS/joined_labels_rounded.txt')

   

    prediction_vector=[]
    for r in range(len(mfcc_vector)):
        prediction=model.predict([(mfcc_vector[r])])
        prediction_vector.append(prediction)


    print(confusion_matrix(labels,prediction_vector))
    print('Recall: '+str(recall_score(labels,prediction_vector)))
    print('Precision: '+str(precision_score(labels,prediction_vector)))
    
    return prediction_vector



def calculate_mfcc(audio,fs):  #Recibo el audio completo, yo creo que es mejor, ya aquí lo parto en frames.
    frame_size=0.01*fs
    number_of_frames=int(len(audio)/frame_size)
    
    mfcc_vector=[]

    for i in range(number_of_frames):
        frame=audio[int(i*frame_size):int(frame_size+i*frame_size)]
        mfcc=librosa.feature.mfcc(y=frame,n_mfcc=13,sr=fs)
        mfcc_vector.append(np.reshape(mfcc,len(mfcc)))

    return mfcc_vector




if __name__=='__main__':
    mfcc_train=np.loadtxt('MFCC_whole_bertso_dataset.txt')
    labels=np.loadtxt('Labels_for_VAD/labels_training_bertso/joined_labels.txt')


    SVM_VAD_training(mfcc_train,labels)
    print('Training finished')
    SVM_VAD_test()
    print('Training finished')

    