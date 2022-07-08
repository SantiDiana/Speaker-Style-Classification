def NotePercentage(vector_notes_detected,f0_cents,cont_voiced):

    cont_percentage=0

    for j in range(len(f0_cents)):
        if vector_notes_detected[j]==1000:
            cont_percentage=cont_percentage+1
        
        if cont_voiced!=0:
            percentage=cont_percentage/cont_voiced
        else:
            percentage=0

    return percentage


