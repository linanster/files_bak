def merge(left, right):
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result

def mergesort(seq):
    Len = len(seq)
    grouplen = 2
    while grouplen < Len*2:
        for i in range(0, Len, grouplen):
            left = seq[i:i+grouplen//2]
            right = seq[i+grouplen//2:i+grouplen]
            seq[i:i+grouplen] = merge(left, right)
        grouplen = grouplen*2

seq = [9,8,7,6,5,4,3,2,1,0]

mergesort(seq)

print(seq)
