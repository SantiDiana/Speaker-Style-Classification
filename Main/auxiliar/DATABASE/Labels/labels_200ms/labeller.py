import numpy as np


labels_frame=[]
for i in range(1,14):
    if i<10:
        labels=np.loadtxt('Main/auxiliar/vectors_folder/f0_sung/f0_cents_0'+str(i)+'_sung.txt')
    else:
        labels=np.loadtxt('Main/auxiliar/vectors_folder/f0_sung/f0_cents_'+str(i)+'_sung.txt')


    longitud=len(labels)
    a = [int(a) for a in str(longitud)]
    print(a)
    print(a[len(a)-1])
    # if a[len(a)-2]<2:
    #     a[len(a)-2]=0
    #     a[len(a)-1]=0
    # elif a[len(a)-2]>=2 and a[len(a)-2]<4:
    #     a[len(a)-2]=2
    #     a[len(a)-1]=0
    # elif a[len(a)-2]>=4 and a[len(a)-2]<6:
    #     a[len(a)-2]=4
    #     a[len(a)-1]=0
    # elif a[len(a)-2]>=6 and a[len(a)-2]<8:
    #     a[len(a)-2]=6
    #     a[len(a)-1]=0
    # else:
    #     a[len(a)-2]=8
    #     a[len(a)-1]=0
    if a[len(a)-2]<5:
        a[len(a)-2]=0
        a[len(a)-1]=0
    else:
        a[len(a)-2]=5
        a[len(a)-1]=0


    longitud=str(a[0])
    for b in range(1,len(a)):
        longitud=longitud+str(a[b])
    
    longitud=int(longitud)


    for z in range(longitud):
        labels_frame.append(labels[z])


for i in range(1,14):
    if i<10:
        labels=np.loadtxt('Main/auxiliar/vectors_folder/f0_spoken/f0_cents_0'+str(i)+'_spoken.txt')
    else:
        labels=np.loadtxt('Main/auxiliar/vectors_folder/f0_spoken/f0_cents_'+str(i)+'_spoken.txt')
    

    longitud=len(labels)
    a = [int(a) for a in str(longitud)]
    print(a)
    print(a[len(a)-1])
    if a[len(a)-2]<5:
        a[len(a)-2]=0
        a[len(a)-1]=0
    else:
        a[len(a)-2]=5
        a[len(a)-1]=0

    longitud=str(a[0])
    for b in range(1,len(a)):
        longitud=longitud+str(a[b])
    
    longitud=int(longitud)


    for z in range(longitud):
        labels_frame.append(labels[z])

np.savetxt('f0_NUS',labels_frame)





