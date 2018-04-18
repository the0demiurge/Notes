# Introduction

I opened this project to show datastructures by hacking `__repr__` function of Python.

Follow my work at [GitHUb](https://github.com/the0demiurge/DataStructureRepr)

# Example


```python
from dsr import BinaryTreeNode

a = BinaryTreeNode(100)
b = BinaryTreeNode(2)
c = BinaryTreeNode(0, a, b)
d = BinaryTreeNode('a', c, c)
a.right = d
a.left = d

print(d)
```

```
                'a'                
               /   \               
          0                   0    
         / \                 / \   
 100         2       100         2 
    \                   \          
     root                root      

```
