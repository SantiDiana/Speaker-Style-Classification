import VAD
import evaluate_pitch
import NoteDetection
import NotePercentage
import NumberFramesPercentage
import SVM
import numpy as np
import pickle
import librosa


def main(path):
    audio_test,fs=librosa.load(path,sr=48000)
   
    filename = 'Main/Parameters_voice_VAD.sav'
    parameters_v= pickle.load(open(filename, 'rb'))

    filename = 'Main/Parameters_silence_VAD.sav'
    parameters_s= pickle.load(open(filename, 'rb'))
    
    mfcc_test=VAD.calculate_mfcc(audio_test,fs) #MFCC calculation frame by frame. 
    vector_binary_test=VAD.test_files(parameters_v,parameters_s,mfcc_test)

    #VAD finished.
    hop_size = int(0.01 * fs)
    #F0 detection algorithm. 
    f0_curve,voiced_flag,voiced_probs=librosa.pyin(audio_test,fmin=librosa.note_to_hz('G1'),fmax=librosa.note_to_hz('C7'),frame_length=hop_size)
    print(len(f0_curve),len(vector_binary_test))
    f0_curve=f0_curve[1:len(f0_curve)]



    f0_curve_treated=evaluate_pitch.f0_treatment(f0_curve,vector_binary_test)   
    #F0 treatment to take into account only the frames labelled as voiced frame to the next parts.
    
    #Note Detection Algorithm
    vector_notes_detected,f0_cents=NoteDetection.NoteDetection(f0_curve_treated)
    
    window=500
    voiced_frame_percentage=NumberFramesPercentage.NumberFramesPercentage(f0_cents,window)
    notes_percentage=NotePercentage.NotePercentage(vector_notes_detected,f0_cents,window)

    vector_through_SVM_voiced=[] #Vector that goes through SVM.
    vector_through_SVM_note=[] #Vector that goes through SVM.

    for i in range(len(voiced_frame_percentage)):
        if voiced_frame_percentage[i]!=0 or notes_percentage[i]!=0:  
            vector_through_SVM_voiced.append(voiced_frame_percentage[i])
            vector_through_SVM_note.append(notes_percentage[i])

    #Prediction of voiced segments.
    prediction_vector=SVM.SVM_prediction(vector_through_SVM_voiced,vector_through_SVM_note) 

    decision_windowed=np.zeros(len(voiced_frame_percentage))  
    c=0
    for i in range(len(voiced_frame_percentage)):
        if  voiced_frame_percentage[i]==0 and notes_percentage[i]==0:
            decision_windowed[i]=0
        else:
            decision_windowed[i]=prediction_vector[c]
            c=c+1

   
    decision_vector=np.zeros(len(f0_cents))  

    for i in range(len(decision_windowed)):
        for j in range(int(i*window/10),int(i*window/10)+int(window/10)):
            if decision_windowed[i]==0:
                    decision_vector[j]=0
            if decision_windowed[i]==1:
                if vector_binary_test[j]==0:  
                    decision_vector[j]=0
                else:
                    decision_vector[j]=1
            if decision_windowed[i]==2:
                if vector_binary_test[j]==0:
                    decision_vector[j]=0
                else:
                    decision_vector[j]=2
    
    rest=len(audio_test)%480
    audio_test=audio_test.tolist()
    audio_test=audio_test[0:len(audio_test)-rest]
    audio_test=audio_test[0:len(audio_test):480]
    
    
    
    
    return decision_vector,audio_test
            

# if __name__=='__main__':
#     decision_vector=main()
    
    