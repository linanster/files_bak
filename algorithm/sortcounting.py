# 计数排序
#
def countingSort(seq):
    maxValue = max(seq)
    countLen = maxValue + 1
    count = [0 for _ in range(countLen)]
    for i in seq:
        count[i]+=1
    sortedIndex = 0
    for i in range(countLen):
        while count[i]>0:
            seq[sortedIndex] = i
            sortedIndex+=1
            count[i]-=1

seq = [1, 3, 4, 5, 2, 6, 9, 7, 8, 0]
countingSort(seq)
print(seq)
