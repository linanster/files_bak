# 希尔排序
def shellSort(seq):
    gapLen = len(seq)//2
    while gapLen > 0:
        for i in range(gapLen, len(seq)):
            # if seq[i-gapLen] > seq[i]:
            insert = seq[i]
            index = i
            while index >= gapLen and seq[index-gapLen] > insert:
                seq[index] = seq[index-gapLen]
                index -= gapLen
            seq[index] =  insert
        gapLen = gapLen//2 

seq = [9,8,7,6,5,4,3,2,1,0]
shellSort(seq)
print(seq)
