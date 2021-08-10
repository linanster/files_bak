def countsort(seq):
    countLen = max(seq) + 1
    count = [0 for _ in range(countLen)]
    for i in seq:
        count[i] += 1
    sortedIndex = 0
    for i in range(countLen):
        while count[i] > 0:
            seq[sortedIndex] = i
            sortedIndex += 1
            count[i] -= 1

seq = [9,8,7,6,5,4,3,2,1,0]

countsort(seq)

print(seq)
