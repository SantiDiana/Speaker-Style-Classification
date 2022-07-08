import numpy as np
import matplotlib.pyplot as plt
import math

def NoteDetection(f0):

    #f0 to cent scale.
    
   
    f0_cents=[]
    fref=440
    for i in range(len(f0)):
        if f0[i]==0:
            f0_cents.append(2500)
        else:
            logarithm=math.log(f0[i]/fref,2)
            formula=1200*logarithm+5800
            f0_cents.append(formula)
        

    #Curve discretization.  
    f0_cents_discretized=np.zeros(len(f0_cents))
    for i in range(len(f0_cents)):
        f0_cents_discretized[i]=round(f0_cents[i],-2)

    #We loop through the signal to see how many voiced segments there are
    m=0
    cont1=0
    cont1_list=[]
    cont1_list.append(0)
    cont2_list=[]
    cont2_list.append(0)
    cont_voiced=0  #Counter of the amount of voiced segments that we have.
    vector_voiced=[]   #Vector of all zeros except numeric values ​​that indicate the number of ones they have before. Vector used to fill when the conditions are met.
    ones_to_be_analyzed=np.zeros(len(f0_cents)) #Vector of values ​​that deserve to be analyzed because they meet the conditions to be analyzed.
    for i in range(1,len(f0_cents)):
        
        if f0_cents[i]!=2500:
            cont1=cont1+1
            cont1_list.append(cont1)

            if i==1:
                cont2_list.append(0)
            else:
                cont2_list.append(cont1_list[i-1])
        else:
            cont1=0
            cont1_list.append(cont1)

            if i==1:
                cont2_list.append(0)
            else:
                cont2_list.append(cont1_list[i-1])

        if  i>1 and cont1==0 and cont2_list[i]>=15:
            cont_voiced=cont_voiced+1
            vector_voiced.append(cont2_list[i])
            for j in range(cont2_list[i]):
                ones_to_be_analyzed[i-j-1]=100
        else:
            vector_voiced.append(0)
            ones_to_be_analyzed[i]=0

    #We now have in ones_to_be_analyzed a vector of the matching voiced frames that are longer than 150ms, 
    # which are the only ones that need to be analyzed. The others are clearly not cataloged as a musical note.
    
    
    
    f0_cents_analyzed=np.zeros(len(f0_cents))  
    for i in range(len(f0_cents)):
        if ones_to_be_analyzed[i]==100:
            f0_cents_analyzed[i]=f0_cents[i]
        else:
            f0_cents_analyzed[i]=2500
    
    
    #Indexes vector where voiced segments start and finish.
    indexes_vector=[]
    for i in range(len(ones_to_be_analyzed)):
        if i==1:
            x=0
        elif ones_to_be_analyzed[i]==100 and ones_to_be_analyzed[i-1]==0:
            indexes_vector.append(i)
        elif ones_to_be_analyzed[i]==0 and ones_to_be_analyzed[i-1]==100:
            indexes_vector.append(i-1)
    
    
    voiced_segment_being_analyzed=[]
    working_vector=[] 
    vector_sizes_notes=[] 
    vector_final_notas_detectadas=np.zeros(len(f0))
    
    for i in range(0,len(indexes_vector),2):
        voiced_segment_being_analyzed=f0_cents_analyzed[indexes_vector[i]:indexes_vector[i+1]]
       
        for j in range(len(voiced_segment_being_analyzed)):  
            
            for y in range(j,len(voiced_segment_being_analyzed)):
                working_vector.append(voiced_segment_being_analyzed[y])
                maximum=max(working_vector)
                minimum=min(working_vector)

                if maximum-minimum>100:
                    vector_sizes_notes.append(len(working_vector))
                    working_vector = []
                    break

        
        if len(vector_sizes_notes)<len(voiced_segment_being_analyzed):  
            vector_sizes_notes.append(len(voiced_segment_being_analyzed)-len(vector_sizes_notes))

        maximum_index=vector_sizes_notes.index(max(vector_sizes_notes)) 
        vector_f0_considered_as_notes=np.zeros(len(voiced_segment_being_analyzed))   
    
        #First high, longest note. With these three lines we find the longest musical note.
        if vector_sizes_notes[maximum_index]>15:
            for a in range(vector_sizes_notes[maximum_index]):
                vector_f0_considered_as_notes[maximum_index+a]=1

        #LEFT PART OF THE MAXIMUM.

        counter_notes_left=2
        maximum_index_work_left=maximum_index
        left_vector_sizes_notes=vector_sizes_notes[0:maximum_index_work_left]
        
        if len(left_vector_sizes_notes)>0:
            izq_max_first_in_left=max(left_vector_sizes_notes)
            izq_max_index_first_in_left=left_vector_sizes_notes.index(izq_max_first_in_left)
        else:
            izq_max_first_in_left=0
            izq_max_index_first_in_left=0

        right_vec_work=[]
        right_max=0
        right_max_index=0
        right_vec_work=left_vector_sizes_notes[izq_max_index_first_in_left+izq_max_first_in_left:maximum_index]
        cont=0
        cont2=0

        while maximum_index_work_left>15 or len(right_vec_work)>15:
            #Treatment of the vector so that there is no overlap
            for u in range(len(left_vector_sizes_notes)):
                if left_vector_sizes_notes[u]>len(left_vector_sizes_notes)-u:
                    left_vector_sizes_notes[u]=len(left_vector_sizes_notes)-u
           
            #Detection new musical note.
            if len(left_vector_sizes_notes)>0:
                left_max=max(left_vector_sizes_notes)
                left_max_index=left_vector_sizes_notes.index(left_max)
            else:
                left_max=0
                left_max_index=0
        
            if left_max>15: # Assignment of the number to the musical note.
                cont=1
                for b in range(left_max):
                    vector_f0_considered_as_notes[left_max_index+b]=counter_notes_left

            # Right part of the left part
            if len(right_vec_work)>0:
                right_max=max(right_vec_work)
                right_max_index=right_vec_work.index(right_max)
            else:
                right_max=0
                right_max_index=0

            if right_max>15:
                cont=cont+1
                for t in range(right_max):
                    vector_f0_considered_as_notes[izq_max_index_first_in_left+izq_max_first_in_left+right_max_index+t]=counter_notes_left+1
                
            maximum_index_work_left=left_max_index
            left_vector_sizes_notes=left_vector_sizes_notes[0:maximum_index_work_left]  
            if cont==1:
                counter_notes_left=counter_notes_left+1
            else:
                counter_notes_left=counter_notes_left+2
        
            right_vec_work=left_vector_sizes_notes[izq_max_index_first_in_left+izq_max_first_in_left+right_max+right_max_index:maximum_index]

        
        #RIGHT PART OF THE MAXIMUM.
        counter_notes_right=counter_notes_left
        maximum_index_work_right=maximum_index
        right_vector_sizes_notes=vector_sizes_notes[maximum_index_work_right+vector_sizes_notes[maximum_index_work_right]:len(vector_sizes_notes)]  

        if len(right_vector_sizes_notes)>0:
            right_max_first=max(right_vector_sizes_notes)
            right_max_index_first=right_vector_sizes_notes.index(right_max_first) 
        else:
            right_max_first=0
            right_max_index_first=0

        if right_max_first>15:
            cont2=1
            for z in range(right_max_first):
                vector_f0_considered_as_notes[maximum_index_work_right+vector_sizes_notes[maximum_index]+right_max_index_first+z]=counter_notes_right

       
        vector_left_of_right=right_vector_sizes_notes[0:right_max_index_first]
        right_v_work=right_vector_sizes_notes[right_max_first+right_max_index_first:len(right_vector_sizes_notes)]
        
        if len(right_v_work)>0:
            m=max(right_v_work) 
                
        if m>15:
            bool=True
        else:
            bool=False
        addition_indexes=0
        addition_maximums=0

        while len(right_v_work)>15 or len(vector_left_of_right)>15 or bool==True:
            #Vector treatment. 
            for g in range(len(vector_left_of_right)):
                if vector_left_of_right[g]>len(vector_left_of_right)-g:
                    vector_left_of_right[g]=len(vector_left_of_right)-g

            
            if len(right_v_work)>0:
                right_max=max(right_v_work)
                right_max_index=right_v_work.index(right_max)
            else:
                right_max=0
                right_max_index=0
            addition_indexes=addition_indexes+right_max_index
            if right_max>15:
                cont2=1
                for o in range(right_max):
                    vector_f0_considered_as_notes[maximum_index+vector_sizes_notes[maximum_index]+right_max_index_first+right_max_first+addition_indexes+addition_maximums+o]=counter_notes_right 
            
            addition_maximums=addition_maximums+right_max
            
            if len(vector_left_of_right)>0:
                left_max=max(vector_left_of_right)
                left_max_index=vector_left_of_right.index(left_max)
            else:
                left_max=0
                left_max_index=0
        

            if left_max>15: # Assignment of the number to the musical note.
                cont2=cont2+1
                for c in range(left_max):
                    vector_f0_considered_as_notes[maximum_index_work_right+vector_sizes_notes[maximum_index_work_right]+left_max_index+c]=counter_notes_right+1

            maximum_index_work_right=maximum_index+vector_sizes_notes[maximum_index_work_right]+right_max_index
            if cont2==1:
                counter_notes_right=counter_notes_right+1
            else:
                counter_notes_right=counter_notes_right+2

            right_v_work=right_vector_sizes_notes[right_max_first+right_max_index_first+addition_maximums+addition_indexes:len(right_vector_sizes_notes)] #Creo que la parte derecha del todo ya está.
            vector_left_of_right=right_vector_sizes_notes[0:left_max_index]
            
            if len(right_v_work)>0:
                m=max(right_v_work) 
            else:
                m=0
                
            if m>15:
                bool=True
            else:
                bool=False

        for x in range(len(vector_f0_considered_as_notes)):
            vector_final_notas_detectadas[indexes_vector[i]+x]=vector_f0_considered_as_notes[x]
        
        vector_f0_considered_as_notes=[]
        vector_sizes_notes=[]
        working_vector=[]


    for i in range(len(vector_final_notas_detectadas)):
        if vector_final_notas_detectadas[i]!=0:
            vector_final_notas_detectadas[i]=1000

    
    print(len(vector_final_notas_detectadas))
        
    return vector_final_notas_detectadas,f0_cents    

def plot_Note_Detection(vector_final_notas_detectadas,f0_cents):   
    vector=range(0,len(f0_cents))
    plt.plot(vector,f0_cents,label='f0 in cents')
    plt.plot(vector,vector_final_notas_detectadas,label='Detected Notes')
    plt.legend(loc='upper right')
    

   

