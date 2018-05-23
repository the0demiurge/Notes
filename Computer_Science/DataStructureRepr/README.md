# Introduction

I opened this project to show datastructures by hacking `__repr__` function of Python.

Follow my work at [GitHUb](https://github.com/the0demiurge/DataStructureRepr)

# Example


```python
print('BinaryTreeNode:')
a = BinaryTreeNode(100)
b = BinaryTreeNode(2)
c = BinaryTreeNode(0, a, b)
d = BinaryTreeNode('a', c, c)
a.right = d
a.left = d

print(d)
print('TreeNode:')
root = TreeNode('tree', [
    TreeNode('types', [TreeNode(str), TreeNode(int)]),
    TreeNode('values', [TreeNode(1), TreeNode(3.1415926), TreeNode(True)]),
    TreeNode('empty'),
    2.718281828,
    'Not TreeNode'
])
print(root)
```
BinaryTreeNode
```
                      ('a')                      
                     /     \                     
              (0)                         (0)    
             /   \                       /   \   
    (100)         (2)           (100)         (2)
   /     \                     /     \           
...       ...               ...       ...        
```
TreeNode
```
('tree')
 ├── ('types')
 │    ├── (<class 'str'>)
 │    └── (<class 'int'>)
 ├── ('values')
 │    ├── (1)
 │    ├── (3.1415926)
 │    └── (True)
 ├── ('empty')
 ├── 2.718281828
 └── 'Not TreeNode'
```
