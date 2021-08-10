def bubblesort(seq):
    Len = len(seq)
    for i in range(Len-1):
        for j in range(0, Len-i-1):
            if seq[j] > seq[j+1]:
                seq[j],seq[j+1] = seq[j+1],seq[j]

seq = [9,8,7,6,5,4,3,2,1,0]

bubblesort(seq)

print(seq)
