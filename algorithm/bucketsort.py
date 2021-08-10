def bucketsort(seq):
    buckentLen = int(max(seq)) + 1
    bucket = {i:[] for i in range(buckentLen)}
    for i in seq:
        bucket[int(i)].append(i)
    seq.clear()
    for v in bucket.values():
        seq.extend(sorted(v))

seq = [9,8,7,6,5,4,3,2,1,0]

bucketsort(seq)

print(seq)
