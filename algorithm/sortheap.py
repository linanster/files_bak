# 思路：
# 根据初始数组去构造初始堆(保证所有的父结点都比它的孩子结点数值大)。
# 每次交换第一个和最后一个元素，然后把剩下元素重新调整为大根堆。

# 将线性数组建模为堆结构
# 对于第i 个元素，它的左节点的下标是(i*2+1)，右节点的下标是(i*2+2)
# 对于第i个元素，他的父节点下标为(i//2+1)

# 将堆中第i个节点与子节点比较，如果子节点中较大者，与父节点交换位置
def heapify(seq, seqLen, i):
    largest = i
    left = 2*i+1
    right = 2*i+2
    if left < seqLen and seq[left] > seq[largest]:
        largest = left
    if right < seqLen and seq[right] > seq[largest]:
        largest = right
    if largest != i:
        seq[i], seq[largest] = seq[largest], seq[i]

# 构建最大堆
def buildMaxHeap(seq, seqLen):
    for i in range(seqLen//2,-1,-1):
        heapify(seq, seqLen, i)

# 堆排序
def heapSort(seq):
    seqLen = len(seq)
    while seqLen > 0:
        buildMaxHeap(seq, seqLen)
        seq[0], seq[seqLen-1] = seq[seqLen-1], seq[0]
        seqLen -= 1

seq = [1, 3, 4, 5, 2, 6, 9, 7, 8, 0]
heapSort(seq)
print(seq)
