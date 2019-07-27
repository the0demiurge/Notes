import random
import sys
import time
sys.setrecursionlimit(1000000)


def quicksort(data, lo, hi):
    if lo >= hi:
        return
    else:
        x = data[lo]
        i, j = lo, hi
        while i < j:
            while x <= data[j] and i < j:
                j -= 1
            data[i] = data[j]
            while x >= data[i] and i < j:
                i += 1
            data[j] = data[i]
        data[i] = x
        quicksort(data, lo, i)
        quicksort(data, i + 1, hi)


# def merge(data, lo, mid, hi):

def mergesort(data, lo, hi):
    pass
    if lo >= hi - 1:
        return
    else:
        mid = (lo + hi) // 2
        mergesort(data, lo, mid), mergesort(data, mid, hi)
        # merge(data, lo, mid, hi)
        if not lo < mid < hi:
            return
        else:
            result = list()
            i, j = lo, mid
            while i < mid and j < hi:
                if data[i] <= data[j]:
                    result.append(data[i])
                    i += 1
                else:
                    result.append(data[j])
                    j += 1
            data[lo:hi] = result + data[i:mid] + data[j:hi]


def main():
    data = [random.randint(0, 1000000) for i in range(20000)]
    d1, d2 = (data.copy() for i in range(2))
    start = time.time()
    quicksort(d1, 0, len(data) - 1)
    print('quicksort', time.time() - start)
    start = time.time()
    mergesort(d2, 0, len(data))
    print('mergesort', time.time() - start)
    start = time.time()
    sorted(data)
    print('timsort in C', time.time() - start)


if __name__ == '__main__':
    main()
