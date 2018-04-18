```python
from reprlib import recursive_repr


class BinaryTreeNode(object):

    def __init__(self, value=None, left=None, right=None):
        self.left, self.right = left, right
        self.value = value

    @recursive_repr(fillvalue='...')
    def __repr__(self):
        result = list()

        repr_left, repr_right = map(
            lambda x: repr(x).split('\n') if x is not None else list(),
            (self.left, self.right))
        repr_self = repr(self.value)

        len_left, len_right = map(
            lambda x: len(x[0]) if len(x) > 0 else 0,
            (repr_left, repr_right))

        height_left, height_right, len_self = map(
            len,
            (repr_left, repr_right, repr_self))

        diff_height = height_left - height_right
        left_bar = ' ' if self.left is None else '/'
        right_bar = ' ' if self.right is None else '\\'

        if diff_height > 0:
            repr_right.extend([' ' * len_right] * diff_height)
        elif diff_height < 0:
            repr_left.extend([' ' * len_left] * (-diff_height))

        result.append(' ' * (len_left + 1) + repr_self + ' ' * (len_right + 1))
        result.append(' ' * (len_left) + left_bar + ' ' * len_self + right_bar + ' ' * len_right)
        result.extend(map(
            lambda x: (' ' * (len_self + 2)).join(x),
            zip(repr_left, repr_right)))

        return '\n'.join(result)
```
```python
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

