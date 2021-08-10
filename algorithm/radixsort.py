def radixsort(seq):
    digitLen = len(str(max(seq)))
    for k in range(digitLen):
        bucket = [[] for _ in range(10)]
        for i in seq:
            bucket[i//(10**k)%10].append(i)
        seq.clear()
        seq.extend([j for i in bucket for j in i])

seq = [9,8,7,6,5,4,3,2,1,0]

radixsort(seq)

print(seq)
