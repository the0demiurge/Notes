## 环境变量

- `readonly`: 设置只读环境变量，禁止修改环境变量
- `unset`: 清除环境变量

## SSH 反向代理

- `ssh -NfR 8080:localhost:80 user@remote_host`
- `autossh -M 23333 -NfR 8080:localhost:80 user@remote_host`

## 查找替换

- `for i in (ag -s 'from' -l);sed 's/from/to/g' $i -i;end`

