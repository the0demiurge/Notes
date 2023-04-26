# Debug

写 C/C++ 和写其他语言相比，最重要的能力之一就是 debug 能力，因为 C/C++ 的 debug 并不容易。

## print/log

简单又通用的方法就是 print 或者写入日志到文件后慢慢分析，进阶一点的方法是使用结构化日志：

1. 按照进程号 - 线程号写入到不同文件（这样写入就不用考虑加锁了）
2. 写入时间、日志记录等级
3. 每个条件判断和函数调用都记录，便于后面 stack trace
4. 使用 lnav 阅读日志

## gdb

只会print/log是很低效的，gdb是个很好用的工具。推荐一个博客：[StormQ’s Blog: 代码调试](https://csstormq.github.io/#jump%E4%BB%A3%E7%A0%81%E8%B0%83%E8%AF%95)。

### 工具篇

gdb 族有很多工具，经过我的测试，比较好用的有如下几个：

1. gdb，这个基本很多环境都自带，肯定要学一下
2. cgdb，和 gdb 基本差不多，但显示效果更好，有语法高亮
3. gdbgui，显示效果非常好，使用 python flask 做个一个网页前端
4. vscode 自带插件可以连接到远程 gdb 或使用 gdb attach 到指定进程

其他还有一些：

- ddd，这个我感觉不是很好用，但是有 gui，可以试试
- lldb，没有实际使用过，和 cgdb 类似，好像对 llvm 适配较高

本文主要使用 cgdb 和 gdb 进行讲解。

### 启动

启动前先说一下，需要使用 Debug 模式编译。

- 从可执行文件启动：
  - `gdb --args <executable-file> <arg1> <arg2> <argn>`
  - `gdb <executable-file>`
- 启动后，连接到正在运行的进程
  - 基于进程号：`sudo gdb --pid <pid>`
  - 基于命令名称：`sudo gdb --pid $(pgrep -n <command name>)`
- 远程调试
  - 启动远程调试服务：`sudo gdbserver --multi :9999 --attach <pid>`
  - 连接到远程调试服务：既然都用远程调试了，当然是为了使用 IDE 自带的功能连上

重要的 gdb 启动参数：

- `--tui`：和 cgdb 类似的代码展示窗口
- `-x <file>`/`-ex <command>`: 启动时执行命令

### Best Practice

首先把常用命令先写到文件中

```gdb
# debug_file.gdb

b some_namespace::SomeClass::some_func
c
n
p <var>
```

`sudo cgdb -- --pid $(pgrep -n <command name>) -x debug_file.gdb`

cgdb 使用 `Esc` 进入源码窗口，使用空格给当前行加断点，使用 `i` 回到 gdb 窗口。

### 常用命令

- 启动配置
  - `set pagination off`：关闭启动提示
  - `set print elements 0`：显示 `...` 的完整内容
  - `set listsize 30`：`l` 命令最大显示行数
- 进程 / 线程
  - `i proc`：看进程、可知性文件情况
  - `i threads`：看线程，注意这里面的线程编号并不是操作系统的线程号
  - `p $_thread`：看断点所在线程
  - `thread <thread-id-by-gdb>` 切换到某线程
  - `thread apply all <command>`：每个线程都运行某指令
- 函数运行状况
  - `bt`/`where`/`bt full`：看堆栈调用层次
  - `bt 1`/`bt -1` 可以指定打印堆栈 traceback 的层次
- `p (rint)`：打印，不光能打印还能赋值；能直接打印整个对象的内容
- 断点
  - 增
    - `b <file-name>:<line-number>`
    - `b <func>`
    - `b *<address>`
    - `b <func> thread <thread-id-by-gdb>`：可以使用 `thread` 命令指定特定线程
    - `b <func> if <expression>`：可以使用 `if` 命令加入条件断点
  - 查
    - `i breakpoints <breakpoint-number>-<breakpoint-number>` 查看断点
  - 删
    - `d breakpoints <breakpoint-number>-<breakpoint-number>` 删除断点，不加参数默认删掉所有
- 运行
  - `l` 显示当前位置，这个命令有 cgdb 后就不需要了
  - `n (ext)`：下一行
  - `ni`/`si`：跳入函数
  - `finish`：跳出函数
  - `c (ontinue)`
- 打印变量
  - `p (rint) <expression>`：不光能直接打印变量 / 对象，还能计算表达式求值，可以调用函数 / 赋值，但调用函数一般用 `call`
  - `display`/`undisplay`/`i display` ：自动打印变量，好像类似于 watch
  - `i args`：打印函数参数
  - `i locals`：打印局部变量
- 函数
  - `call <function-name>`
  - `return <return-value>`
