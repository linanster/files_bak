# 折半查找
def bisearch(seq, lower, upper, num):
    if lower>upper:
        return -1
    elif lower==upper:
        try:
            assert seq[lower] == num
        except AssertionError:
            return -1
        else:
            return lower
    else:
        mid = (lower+upper)//2
        if num == seq[mid]:
            return mid
        elif num < seq[mid]:
            return bisearch(seq, lower, mid-1, num)
        else:
            return bisearch(seq, mid+1, upper, num)


l1 = [0,1,2,3,4,5]

print(bisearch(l1, 0, len(l1)-1, 3))
