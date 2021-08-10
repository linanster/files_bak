def shellsort(seq):
    Len = len(seq)
    gaplen = Len//2
    while gaplen >= 1:
        for i in range(gaplen, Len):
            index = i
            insert = seq[i]
            while index>=gaplen and seq[index-gaplen]>insert:
                seq[index] = seq[index-gaplen]
                index -= gaplen
            seq[index] = insert
        gaplen = gaplen//2

seq = [9,8,7,6,5,4,3,2,1,0]

shellsort(seq)

print(seq)
