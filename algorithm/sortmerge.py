# 归并排序
def mergeSort(seq): 
    if len(seq) <= 1:
        return seq
    mid = len(seq)//2
    left = seq[:mid]
    right = seq[mid:]
    return merge(mergeSort(left), mergeSort(right))

def merge(left, right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result

seq = [2,4,3,5,1]

print(mergeSort(seq))

