# 桶排序
# https://www.runoob.com/w3cnote/bucket-sort.html
#
def bucketSort(seq, maxValue):
    buf = {i:[] for i in range(int(maxValue)+1)}
    for i in seq:
        buf[int(i)].append(i)
    seq = []
    for v in buf.values():
        if v:
            seq.extend(sorted(v))
    return seq


lis = [3.1, 4.2, 3.3, 3.5, 2.2, 2.7, 2.9, 2.1, 1.55, 4.456, 6.12, 5.2, 5.33, 6.0, 2.12]
print(bucketSort(lis, max(lis)))
