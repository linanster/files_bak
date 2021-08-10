def quicksort(seq):
    Len = len(seq)
    if Len <= 1:
        return seq
    pivot = seq[0]
    lesser = [x for x in seq[1:] if x < pivot]
    greater = [x for x in seq[1:] if x >= pivot]
    return quicksort(lesser) + [pivot,] + quicksort(greater)

seq = [9,8,7,6,5,4,3,2,1,0]

print(quicksort(seq))
