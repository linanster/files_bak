# 希尔排序
def shellSort(seq):
    gap = len(seq)//2
    while gap > 0:
        for i in range(gap, len(seq)):
            # if seq[i-gap] > seq[i]:
            insert = seq[i]
            index = i
            while index >= gap and seq[index-gap] > insert:
                seq[index] = seq[index-gap]
                index -= gap
            seq[index] =  insert
        # print(seq)
        gap = gap//2 

seq = [9,8,7,6,5,4,3,2,1,0]
shellSort(seq)
print(seq)
