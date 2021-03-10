# 插入排序
def insertionSort(seq):
    for i in range(1, len(seq)):
        if seq[i-1] > seq[i]:
            index = i
            insert = seq[i]
            while index>0 and seq[index-1]>insert:
                seq[index] = seq[index-1]
                index -= 1
            seq[index] = insert

seq = [2,4,1,5,3]

insertionSort(seq)
print(seq)

