# 实验室服务器运维脚本

### sendlog.py

将服务器日志发送到指定邮箱

### charles-adduser.sh

添加用户时顺便记录时间和是谁

### backup_server_data.py

使用scp将服务器某些地方的数据送到另一个服务器的某些位置。
### mv2cron.sh

将上面的脚本放到服务器中/cron.hourly, /cron.daily, ...然后编辑相关位置，使得可以正常地备份
### 如果服务器出了问题：

去备份位置寻找以前的备份，并想办法恢复备份
### 想要使用本脚本，你需要学习：
1. ssh免密码登陆
2. scp使用方法
3. crontab的用法和/etc/cron.daily等相关文件夹
4. 初步学会bash脚本的用法（和写法）
5. vi的用法
### 其他
- 你可能需要在命令行登陆 ip 网关，可以使用[东北大学 ip 网关登陆器](https://github.com/the0demiurge/CharlesScripts/blob/master/charles/bin/ipgw)
