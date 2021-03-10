# 冒泡排序
def bubbleSort(seq):
    for i in range(len(seq)-1):
        for j in range(len(seq)-i-1):
            if seq[j] > seq[j+1]:
                seq[j], seq[j+1] = seq[j+1], seq[j]

seq = [2,4,3,5,1]

bubbleSort(seq)
print(seq)
