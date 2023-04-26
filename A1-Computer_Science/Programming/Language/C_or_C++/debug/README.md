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
