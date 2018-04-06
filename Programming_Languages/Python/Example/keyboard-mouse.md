# Python监听终端

```python
import sys
import tty
import termios


def detectFocusedTerminal():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char
```
# Python 全局捕获键盘

```python
from evdev import InputDevice, list_devices
from select import select


def detectInputKey():
    dev = InputDevice('/dev/input/event4')
    print(dev)
    while True:
        select([dev], [], [])
        for event in dev.read():
            print("code:%s value:%s" % (event.code, event.value))
```
# Python 全局捕获鼠标

```python

import struct
mou = open("/dev/input/mice", "rb")


def m_event():
    m = mou.read(3)
    b = ord(m[0])
    bl = b & 0x1
    bm = (b & 0x4) > 0
    br = (b & 0x2) > 0
    x, y = struct.unpack("bb", m[1:])
    print("Left:%d, Middle: %d, Right: %d, x: %d, y: %d\n" % (bl, bm, br, x, y)          )


while(1):
m_event()
mou.close()
```