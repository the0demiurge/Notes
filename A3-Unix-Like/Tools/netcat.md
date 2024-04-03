# 传输文件

- 发送：`tar cvzf - <files>|nc <ip> <port>`
- 接收：`nc -l <port>|tar xvzf -`