```python
from collections import deque
from dsr import BinaryTreeNode as Node


def dfs(root):
    s = list()

    s.append(root)
    
    while len(s) > 0:
        r = s.pop()
        if r is None:
            continue
        print(r.value, end=' ')
        s.append(r.right)
        s.append(r.left)
    print()


def bfs(root):
    q = deque()

    q.append(root)
    
    while len(q) > 0:
        r = q.pop()
        if r is None:
            continue
        print(r.value, end=' ')
        q.appendleft(r.left)
        q.appendleft(r.right)
    print()


def main():
    root = Node(
        1,
        Node(
            2,
            Node(4),
            Node(5)
        ),
        Node(
            3,
            Node(6),
            Node(7)
        )
    )
    print('tree:', root, sep='\n')
    print('dfs:')
    dfs(root)
    print('bfs:')
    bfs(root)


if __name__ == "__main__":
    main()
```

## Results:

```
tree:
            (1)            
           /   \           
    (2)             (3)    
   /   \           /   \   
(4)     (5)     (6)     (7)
dfs:
1 2 4 5 3 6 7 
bfs:
1 2 3 4 5 6 7 
```

