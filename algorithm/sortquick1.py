# 快速排序
def qSort(seq):
    if seq == []:
        return seq
    pivot = seq[0]
    lesser = [x for x in seq[1:] if x <= pivot]
    greater = [x for x in seq[1:] if x > pivot]
    return qSort(lesser) + [pivot] + qSort(greater)

seq = [2,4,3,5,1]
print(qSort(seq))
