```bash
#!/bin/bash
# 将$1所指定的脚本分别复制到crontab中不同的备份周期文件夹，并逐个编辑相关备份脚本
cp $1 /etc/cron.hourly
cp $1 /etc/cron.daily
cp $1 /etc/cron.weekly
cp $1 /etc/cron.monthly
vi /etc/cron.hourly/$1
vi /etc/cron.daily/$1
vi /etc/cron.weekly/$1
vi /etc/cron.monthly/$1
ls /etc/cron.hourly
ls /etc/cron.daily
ls /etc/cron.weekly
ls /etc/cron.monthly
```