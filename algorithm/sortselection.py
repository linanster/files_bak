# 选择排序
def selectionSort(seq):
    for i in range(len(seq)-1):
        index = i
        for j in range(i+1, len(seq)):
            if seq[j] < seq[index]:
                index = j
        # if index != i:
        seq[i], seq[index] = seq[index], seq[i]

seq = [9,8,7,6,5,4,3,2,1,0]
selectionSort(seq)
print(seq)
