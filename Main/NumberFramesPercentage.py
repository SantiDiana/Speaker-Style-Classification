#Last version of the Number Frames Percentage which is used in the training and test of the SVM.
import numpy as np

def NumberFramesPercentage(f0_cents,window):

    frame_size=10
    n_frames_window=int(window/frame_size)

    cont_voiced=0
    percentages_vector=[]

    for i in range(n_frames_window,len(f0_cents),n_frames_window):
        for j in range(n_frames_window):
            if f0_cents[i-j]!=2500:
                cont_voiced=cont_voiced+1
            
        
        if cont_voiced!=0:
            percentage=cont_voiced/n_frames_window
        else:
            percentage=0
        percentages_vector.append(percentage)
        percentage=0
        cont_voiced=0
    
    return percentages_vector
        


if __name__=='__main__':
    
    f0=np.loadtxt('auxiliar/DATABASE/Labels/labels_200ms/whole_bertso_f0_cents.txt')
    window=200

    percentages_vector=NumberFramesPercentage(f0,window)
    np.savetxt('auxiliar/DATABASE/Labels/labels_200ms/whole_bertso_voiced_percentage.txt',percentages_vector)

