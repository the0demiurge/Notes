```python
from reprlib import recursive_repr


class TreeNode(object):
    __slots__ = ("value", "children")

    def __init__(self, value=None, children=None):
        self.value = value
        self.children = list() if children is None else children

    @recursive_repr(fillvalue='...')
    def __repr__(self):
        root = '(' + repr(self.value) + ')'
        if not self.children:
            return root
        result = [root]
        for child in self.children[:-1]:
            result.append(self.__build_child_repr(child, end=False))
        result.append(self.__build_child_repr(self.children[-1], end=True))
        return '\n'.join(result)

    @staticmethod
    def __build_child_repr(child, end=False):
        child_repr = repr(child).split('\n')
        fork, space = (' └── ', '     ') if end else (' ├── ', ' │   ')
        return '\n'.join([fork + child_repr[0]] + list(map(lambda x: space + x, child_repr[1:])))
```

