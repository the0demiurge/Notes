#!/usr/bin/python3
"""介绍：将backup_from列表内的文件通过scp备份到远程服务器的backup_to文件夹。
"""
import os
import time

# set the backup informations
backup_len = 1 # 备份数量
backup_from = ['/opt/discuz-data/data/']
backup_ssh_user = 'root@abc.net'
backup_ssh_port = '8022'
backup_to = '/data/backup/discuz/weekly'
identity_file = '/root/.ssh/id_rsa'

now = time.strftime('%Y-%m-%d_%X', time.localtime(time.time()))

os.system('ssh -p {backup_ssh_port} -i {identity_file} {backup_ssh_user} -T "mkdir -p {backup_to}/{now}"'.format(
    identity_file=identity_file,
    backup_ssh_port=backup_ssh_port,
    backup_ssh_user=backup_ssh_user,
    backup_to=backup_to,
    now=now))

for path_i in backup_from:
    os.system("scp -p -P {backup_ssh_port} -i {identity_file} -r {backup_from} {backup_ssh_user}:{backup_to}/{now}".format(
        identity_file=identity_file,
        backup_ssh_port=backup_ssh_port,
        backup_from=path_i,
        backup_ssh_user=backup_ssh_user,
        backup_to=backup_to,
        now=now))

pipe = os.popen('ssh -p {backup_ssh_port} -i {identity_file} {backup_ssh_user} -T "ls {backup_to}"'.format(
    identity_file=identity_file,
    backup_ssh_port=backup_ssh_port,
    backup_ssh_user=backup_ssh_user,
    backup_to=backup_to), 'r', -1)
pathes = []
for i in pipe:
    pathes.append(i.strip())

pathes.sort()
print(pathes)
if len(pathes) > backup_len:
    for i in pathes[:-backup_len]:
        os.system("ssh -p {backup_ssh_port} -i {identity_file} -T {backup_ssh_user} 'rm -rf {backup_to}/{now}'".format(
            identity_file=identity_file,
            backup_ssh_user=backup_ssh_user,
            backup_ssh_port = backup_ssh_port,
            backup_to=backup_to,
            now=i))

