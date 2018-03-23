## Source Code

### args.c

```c
#include <stdio.h>

int main(int argc, char** argv){
  for(int i=0; i<argc; i++)
  printf("num: %5d, %s\n", i, * (argv + i));
  return argc;
}
```

```bash
gcc -olibapgs.so -shared -fPIC args.c
```

### args.py

```python
from ctypes import *

handler = CDLL('./libargs.so')
handler.main.argtypes = (c_int, POINTER(POINTER(c_char)))
handler.main.restype = (c_int)

args = b'aoue .uao ainst nhn'.split()

argc = len(args)

argv = (POINTER(c_char) * argc)(* map(create_string_buffer, args))
h = handler.main(argc, argv)

print(h)
```

---

## Result

```bash
python args.py
```



```
num:     0, aoue
num:     1, .uao
num:     2, ainst
num:     3, nhn
4
```

