# 归并排序
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
    groupLen = 2
    while groupLen < len(seq)*2:
        for i in range(0, len(seq), groupLen):
            left = seq[i : i+groupLen//2]
            right = seq[i+groupLen//2 : i+groupLen]
            seq[i:i+groupLen] = merge(left, right)
        groupLen *= 2

seq = [9,8,7,6,5,4,3,2,1,0]
mergeSort(seq)
print(seq)


