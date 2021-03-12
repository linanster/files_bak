# 插入排序
#
def insertionSort(seq):
    for i in range(1, len(seq)):
        # if seq[i-1] > seq[i]:
        index = i
        insert = seq[i]
        while index>=1 and seq[index-1]>insert:
            seq[index] = seq[index-1]
            index -= 1
        seq[index] = insert

seq = [9,8,7,6,5,4,3,2,1,0]

insertionSort(seq)
print(seq)

