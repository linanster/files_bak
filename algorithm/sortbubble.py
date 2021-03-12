# 冒泡排序
def bubbleSort(seq):
    for i in range(len(seq)-1):
        for j in range(len(seq)-i-1):
            if seq[j] > seq[j+1]:
                seq[j], seq[j+1] = seq[j+1], seq[j]

seq = [9,8,7,6,5,4,3,2,1,0]

bubbleSort(seq)
print(seq)
