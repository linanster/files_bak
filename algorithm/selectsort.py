def selectsort(seq):
    Len = len(seq)
    for i in range(Len-1):
        index = i
        for j in range(i+1, Len):
            if seq[j] < seq[index]:
                index = j
        seq[index],seq[i] = seq[i],seq[index]

seq = [9,8,7,6,5,4,3,2,1,0]

selectsort(seq)

print(seq)
