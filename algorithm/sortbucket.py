# 桶排序
# https://www.runoob.com/w3cnote/bucket-sort.html
#
def bucketSort(seq):
    maxValue = max(seq)
    bucketLen = int(maxValue)+1
    bucket = {i:[] for i in range(bucketLen)}
    for i in seq:
        bucket[int(i)].append(i)
    seq.clear()
    for v in bucket.values():
        # if v:
        seq.extend(sorted(v))


seq = [3.1, 4.2, 3.3, 3.5, 2.2, 2.7, 2.9, 2.1, 1.55, 4.456, 6.12, 5.2, 5.33, 6.0, 2.12]
bucketSort(seq)
print(seq)
