from Main.evaluate_pitch import f0_treatment
import VAD_rt
import evaluate_pitch_rt
import NoteDetection_rt
import NotePercentage_rt
import NumberFramesPercentage_rt
import SVM_rt
import numpy as np
import pickle
import pitch_extractor
import librosa
import math

import matplotlib.pyplot as plt

def main(audio_test,fs,parameters_v,parameters_s):
    

    mfcc_test=VAD_rt.calculate_mfcc(audio_test,fs) #MFCC calculation frame by frame. 
    vector_binary_test=VAD_rt.test_files(parameters_v,parameters_s,mfcc_test)

    # print('audio')
    # print(audio_test)

    # print('Binary vector')
    # print(vector_binary_test)

    #VAD finished.
    hop_size = int(0.01 * fs)
    #F0 detection algorithm. 
    p_e=pitch_extractor.PitchExtractor()
    f0_curve,confidence,_=p_e.extract_as_hz(audio_test, fs, hop_size, 'DNN', audio_filepath='', frame_size=hop_size)
    # print('F0 curve below')
    # print(f0_curve)
    
    f0_curve_treated=evaluate_pitch_rt.f0_treatment(f0_curve,vector_binary_test)
    for y in range(4):
        f0_curve_treated[16+y]=f0_curve_treated[15]   
    # print('F0 curve treated below')
    # print(f0_curve_treated)
    #F0 treatment to take into account only the frames labelled as voiced frame to the next parts.
    
    #Note Detection Algorithm
    cont_voiced=0
    for i in range(len(f0_curve_treated)):
        if f0_curve_treated[i]!=0:
            cont_voiced=cont_voiced+1

    vector_notes_detected=np.zeros(len(f0_curve_treated))
    f0_cents=[]
    fref=440
    for i in range(len(f0_curve_treated)):
        if f0_curve_treated[i]==0:
            f0_cents.append(2500)
        else:
            logarithm=math.log(f0_curve_treated[i]/fref,2)
            formula=1200*logarithm+5800
            f0_cents.append(formula)

    # print('F0 cents')
    # print(f0_cents)
    # print('Talking counter: '+str(cont_voiced))
    

    if cont_voiced>=15:
        vector_notes_detected=NoteDetection_rt.NoteDetection(f0_cents,vector_binary_test)
    
    
    # print('Notes detected below')
    # print(vector_notes_detected)
    
    
    voiced_frame_percentage=NumberFramesPercentage_rt.NumberFramesPercentage(f0_cents)
    notes_percentage=NotePercentage_rt.NotePercentage(vector_notes_detected,f0_cents,cont_voiced)
    
    # print('Both parameters')
    # print(voiced_frame_percentage,notes_percentage)

   
    if voiced_frame_percentage!=0 or notes_percentage!=0:  
        vector_through_SVM_voiced=voiced_frame_percentage
        vector_through_SVM_note=notes_percentage
        prediction=SVM_rt.SVM_prediction(vector_through_SVM_voiced,vector_through_SVM_note)


    #Prediction of voiced segments.
    

    if  voiced_frame_percentage==0 and notes_percentage==0:
        decision_windowed=0
    else:
        decision_windowed=prediction
        
    decision_vector=np.empty(len(f0_cents),dtype='str')  

    for j in range(len(f0_cents)):
        if decision_windowed==0:
                decision_vector[j]=0
        if decision_windowed==1:
            if vector_binary_test[j]=='Silence':  
                decision_vector[j]=0
            else:
                decision_vector[j]=1
        if decision_windowed==2:
            if vector_binary_test[j]=='Silence':
                decision_vector[j]=0
            else:
                decision_vector[j]=2
    

    return decision_vector
            


    
    