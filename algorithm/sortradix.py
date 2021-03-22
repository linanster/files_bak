# 基数排序
#
def radixSort(seq):
    digitLen = len(str(max(seq)))
    for k in range(digitLen):
        bucket = [[] for _ in range(10)]
        for i in seq:
            bucket[i//(10**k)%10].append(i)
        seq.clear()
        seq.extend([j for i in bucket for j in i])

seq = [334,5,67,345,7,345345,99,4,23,78,45,1,3453,23424]
radixSort(seq)
print(seq)
