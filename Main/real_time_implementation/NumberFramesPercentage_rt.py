#Last version of the Number Frames Percentage which is used in the training and test of the SVM.
import numpy as np

def NumberFramesPercentage(f0_cents):

    cont_voiced=0
    for j in range(len(f0_cents)):
        if f0_cents[j]!=2500:
            cont_voiced=cont_voiced+1
            
        if cont_voiced!=0:
            percentage=cont_voiced/len(f0_cents)
        else:
            percentage=0
        
    return percentage
        


# if __name__=='__main__':
    
#     f0=np.loadtxt('auxiliar/DATABASE/Labels/labels_200ms/whole_bertso_f0_cents.txt')
#     window=200

#     percentages_vector=NumberFramesPercentage(f0,window)
#     np.savetxt('auxiliar/DATABASE/Labels/labels_200ms/whole_bertso_voiced_percentage.txt',percentages_vector)

