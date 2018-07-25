# 将 py 编译为可执行文件

```bash
cython --emded -3 main.py -o main.c
gcc $(python-config --cflags) $(python-config --ldflags) ./main.c -o main
```

# 将 py 编译为可被 python import 的共享库

```python
# setup.py
from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize('/path/to/file.py'))
```

```bash
python setup.py build
```

然后可以直接把编译成的二进制 so 文件当作 py 脚本导入运行