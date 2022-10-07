import matplotlib.pyplot as plt 

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
    


    