# 快速排序
def qSort(seq, low1, high1):
    if low1 >= high1:
        pass
    else:
        low = low1
        high = high1
        pivot = seq[low]
        while low < high:
            while low < high and seq[high] >= pivot:
                high -= 1
            seq[low] = seq[high]
            while low < high and seq[low] <= pivot:
                low += 1
            seq[high] = seq[low]
        seq[low] = pivot

seq = [2,4,3,5,1,]
qSort(seq, 0, 4)
print(seq)
