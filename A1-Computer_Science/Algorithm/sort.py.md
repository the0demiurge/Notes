# Sort in Python

## QuickSort and MergeSort

### Code

```python
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
```
### Result

```
quicksort 0.06924867630004883
mergesort 0.10277152061462402
timsort in C 0.0060214996337890625
```
## BinaryTreeSort

### Code

```python
import random
from dsr import BinaryTreeNode as Node


class BinarySortTree(object):
    def __init__(self, data=list()):
        self.root = Node()
        for val in data:
            self.insert(val)

    def insert(self, val):
        if self.root.value is None:
            self.root.value = val
            return
        leaf, root = (self.root,)*2
        while root is not None:
            leaf = root
            if root.value > val:
                root = root.left
            else:
                root = root.right
        if leaf.value > val:
            leaf.left = Node(val)
        else:
            leaf.right = Node(val)

    def traverse(self, root=False):
        if root is False:
            root = self.root
        if root is None:
            return list()
        return self.traverse(root.left) + [root.value] + self.traverse(root.right)

    def __repr__(self):
        return repr(self.root)


data = [random.randint(0, 100) for i in range(10)]
print(data)
tree = BinarySortTree(data)
print(tree)
print(tree.traverse())
```
### Result

```
[36, 43, 26, 9, 73, 76, 73, 72, 31, 19]
                    (36)                           
                   /    \                          
          (26)            (43)                     
         /    \               \                    
 (9)           (31)                 (73)           
    \                              /    \          
     (19)                      (72)           (76) 
                                             /     
                                         (73)      
[9, 19, 26, 31, 36, 43, 72, 73, 73, 76]
```