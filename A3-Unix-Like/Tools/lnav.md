# lnav

这个命令是我在 linux 上面发现的特别好用的日志查看器，可以自动整合多日志文件，自动合并 logrotate 文件，还能自动解压缩。

这个命令可以配合 [logging](../../A1-Computer_Science/Programming/Language/Python/Example/logging.md) 模块使用。

## 常用功能

- 命令行参数
  - `-r` 递归检索整个文件夹
  - `-R` 也看 logrotate 的旧日志
- 快捷键
  - 筛选
    - `:set-min-log-level <level>`
    - `tab` 日志筛选器，使用`i/o`创建正向或反向筛选，`D`删掉筛选器
    - `Ctrl+F` toggle
  - `m/M/C` 标记，对于标记的内容可以进行文件操作，这个非常好用
    - `:append-to`, `write-to`, `write-csv-to`, `write-json-to`, `pipe-to`, `pipe-line-to`
  - 显示
    - `P` pretty print
    - `Ctrl+L` 拷贝模式
    - `Ctrl+W` 折行
    - `i/I` 统计，`z/Z` 切换统计尺度
  - 浏览/跳转
    - `e/E` error
    - `w/W` warning
    - `n/N, >/<`搜索
    - `s/S` 查找日志记录减缓的时刻
    - 时间跳转
      - `d/D`24h跳转
      - `1-6/Shift 1-6` 十分钟跳转
      - `7-8` 分钟跳转
      - `0/Shift 0`日期跳转（日界线）
      - `:goto a minute later`, `:relative-goto` + `r/R` 重复操作

## 其他命令

- `:unix-time <secs-or-date>`, `:current-time`转换 timestamp
- `:comment`, `:clear-comment`, `:tag`, `:untag`, `:delete-tags`
