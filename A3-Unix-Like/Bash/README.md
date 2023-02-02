## 环境变量

- `readonly`: 设置只读环境变量，禁止修改环境变量
- `unset`: 清除环境变量

## SSH 反向代理

- `ssh -NfR 8080:localhost:80 user@remote_host`
- `autossh -M 23333 -NfR 8080:localhost:80 user@remote_host`

## 查找替换

- `for i in (ag -s 'from' -l);sed 's/from/to/g' $i -i;end`

## 按行遍历

如果用`for ITEM in $(ls -l)`，是按词遍历的，for事先就把item按照空格分隔了。这种时候需要使用`ls -l|while read LINE`，使用read读取一整行，并存到变量`$LINE`中
