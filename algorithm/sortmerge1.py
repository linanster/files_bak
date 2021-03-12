# 归并排序(递归, out-place)
#
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

def mergeSort(seq): 
    if len(seq) <= 1:
        return seq
    mid = len(seq)//2
    left = seq[:mid]
    right = seq[mid:]
    return merge(mergeSort(left), mergeSort(right))

seq = [9,8,7,6,5,4,3,2,1,0]

print(mergeSort(seq))

