import numpy as np
from sklearn import svm
import pickle




def SVM_training():  
    
    vector_percentages_voiced=np.loadtxt('Main/auxiliar/DATABASE/Labels/vector_porcentajes_voiced_completa_bertso_training.txt')
    vector_percentages_notes=np.loadtxt('Main/auxiliar/DATABASE/Labels/vector_porcentajes_notes_completa_bertso_training.txt')
    labels=np.loadtxt('Main/auxiliar/DATABASE/Labels/labels_whole_bertso_training.txt')
    vector_both_parameters=[]
   

    for i in range(len(vector_percentages_voiced)):
        v=vector_percentages_voiced[i],vector_percentages_notes[i]
        vector_both_parameters.append(v)


    model=svm.SVC(kernel='linear',class_weight='balanced')
    model.fit(vector_both_parameters,labels)
    print('Modelo SVM entrenado')

    filename = 'Main/finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))



   


def SVM_prediction(vector_percentages_voiced,vector_percentages_notes):  

    vector_both_parameters=[]

    for i in range(len(vector_percentages_voiced)):
        v=vector_percentages_voiced[i],vector_percentages_notes[i]
        vector_both_parameters.append(v)

    filename = 'Main/finalized_model.sav'
    model = pickle.load(open(filename, 'rb'))

    prediction_vector=[]
    for r in range(len(vector_both_parameters)):
        prediction=model.predict([(vector_both_parameters[r])])
        prediction_vector.append(prediction)

    return prediction_vector


   

def SVM_test():  

    vector_percentages_voiced=np.loadtxt('Main/auxiliar/DATABASE/Labels/labels_NUS_training_and_test/vector_porcentajes_voiced_completa.txt')
    vector_percentages_notes=np.loadtxt('Main/auxiliar/DATABASE/Labels/labels_NUS_training_and_test/vector_porcentajes_notes_completa.txt')
    labels=np.loadtxt('Main/auxiliar/DATABASE/Labels/labels_NUS_training_and_test/labels_whole_NUS.txt')

    vector_both_parameters=[]

    for i in range(len(vector_percentages_voiced)):
        v=vector_percentages_voiced[i],vector_percentages_notes[i]
        vector_both_parameters.append(v)


    filename = 'Main/finalized_model.sav'
    model = pickle.load(open(filename, 'rb'))
    
    prediction_vector=[]
    for r in range(len(vector_both_parameters)):
        prediction=model.predict([(vector_both_parameters[r])])
        prediction_vector.append(prediction)
  

    TP=0
    FP=0
    TN=0
    FN=0
    
    for i in range(len(vector_percentages_voiced)):
        if prediction_vector[i]==1 and labels[i]==1:
            TP=TP+1
        elif prediction_vector[i]==1 and labels[i]==2:
            FP=FP+1
        elif prediction_vector[i]==2 and labels[i]==2:
            TN=TN+1
        elif prediction_vector[i]==2 and labels[i]==1:
            FN=FN+1
        
    precision=TP/(TP+FP)
    recall=TP/(TP+FN)
    accuracy=(TP+TN)/(TP+TN+FN+FP)
    f_score=(2*precision*recall)/(precision+recall)

    print('Metrics for the SVM only: '+str(f_score),str(accuracy),str(recall),str(precision))
    prediction_vector=np.reshape(prediction_vector,-1)

    return prediction_vector





    
