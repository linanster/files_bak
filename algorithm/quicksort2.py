def quicksort(seq, low1, high1):
    if low1 >= high1:
        return
    low = low1
    high = high1
    pivot = seq[low]
    while low < high:
        while low < high and seq[high] >= pivot:
            high -= 1
        seq[low] = seq[high]
        while low < high and seq[low]  <= pivot:
            low += 1
        seq[high] = seq[low]
    seq[low] = pivot
    quicksort(seq, low1, low-1)
    quicksort(seq, low+1, high1)

seq = [9,8,7,6,5,4,3,2,1,0]

quicksort(seq, 0, len(seq)-1)

print(seq)
