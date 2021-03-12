# 快速排序(递归, out-place)
#
def qSort(seq):
    if len(seq) <= 1:
        return seq
    pivot = seq[0]
    lesser = [x for x in seq[1:] if x <= pivot]
    greater = [x for x in seq[1:] if x > pivot]
    return qSort(lesser) + [pivot] + qSort(greater)

seq = [9,8,7,6,5,4,3,2,1,0]
print(qSort(seq))
