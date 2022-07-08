#Last version of the Note Percentage Algorithm which is used in the training and test of the SVM.


def NotePercentage(vector_notes_detected,f0_cents,window):

    frame_size=10
    n_frames_window=int(window/frame_size)
    
    percentages_vector=[]
    cont_voiced=0
    cont_percentage=0

    for i in range(n_frames_window,len(vector_notes_detected),n_frames_window):
        for j in range(n_frames_window):
            if f0_cents[i-j]!=2500:
                cont_voiced=cont_voiced+1
            if vector_notes_detected[i-j]==1000:
                cont_percentage=cont_percentage+1
        
        if cont_voiced!=0:
            percentage=cont_percentage/cont_voiced
        else:
            percentage=0
        percentages_vector.append(percentage)
        percentage=0
        cont_voiced=0
        cont_percentage=0

    return percentages_vector


