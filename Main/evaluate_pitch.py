import os
import sys
import librosa
import pitch_extractor
import matplotlib.pyplot as plt 
import numpy as np
#import pyworld as pw
def f0_extraction(audio_folder):

    
    ## Check if input folder exists and build wav list
    if os.path.exists(audio_folder):
        file_list = [x for x in os.listdir(audio_folder) if x.endswith(".wav") and not x.startswith(".")]
    else:
        print("Input audio folder does not exist. Please check path")
        sys.exit(-1)

    sample_rates = [48000] # in Hz
    time_steps = [0.01] # in seconds
    thresholds = [0.7] # confidence threshold above which a segment is considered voiced or not
  

    for sample_rate in sample_rates:
        for hop_time in time_steps:
            for file_name in file_list:
                input_filepath = os.path.join(audio_folder, file_name)
                audio, sr = librosa.load(input_filepath, sample_rate)
                file_name_no_ext = os.path.splitext(file_name)[0]
                hop_size = int(hop_time * sr)

                ## Evaluate pitch
                pitch_hz, confidence, timer = pitch_extractor.PitchExtractor().extract_as_hz(audio, sr, hop_size, 'DNN', audio_filepath=input_filepath, frame_size=hop_size)
                # print(pitch_hz)
                # print(confidence)

                return pitch_hz,confidence
                

# def world(audio_folder,file_name):
#     sample_rate=48000
#     hop_time=10
#     input_filepath = os.path.join(audio_folder, file_name)
#     audio, sr = librosa.load(input_filepath, sample_rate)
#     audio_double = audio.astype(np.double)
#     ## Compute WORLD features
#     f0, sp, ap = pw.wav2world(audio_double, sr,frame_period=hop_time)

#     return f0

def f0_treatment(f0_curve,vector_binary_test):
 
    dnn_confidence_tested=[]
    for i in range(len(vector_binary_test)):
        if vector_binary_test[i]==1:
              dnn_confidence_tested.append(f0_curve[i])
        else:
             dnn_confidence_tested.append(0)
    
    return dnn_confidence_tested


    
def plot_f0(dnn_confidence_tested,label):
    vector2=range(0,len(dnn_confidence_tested))
    plt.plot(vector2,dnn_confidence_tested,label=label)

    plt.ylabel('Hz')
    plt.xlabel('Frames')
    plt.legend(loc='upper right')
    


    