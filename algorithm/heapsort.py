def heapify(seq, Len, i):
    largest = i
    left = 2*i + 1
    right = 2*i + 2
    if left < Len and seq[left] > seq[largest]:
        largest = left
    if right < Len and seq[right] > seq[largest]:
        largest = right
    if largest != i:
        seq[i], seq[largest] = seq[largest], seq[i]

def buildMaxHeap(seq, Len):
    for i in range(Len//2, -1, -1):
        heapify(seq, Len, i)

def heapsort(seq):
    Len = len(seq)
    for sublen in range(Len, 1, -1):
        buildMaxHeap(seq, sublen)
        seq[0], seq[sublen-1] = seq[sublen-1], seq[0]

seq = [9,8,7,6,5,4,3,2,1,0]

heapsort(seq)

print(seq)
