# 磁盘配额设置

## 启动配额
1. 编辑 `/etc/fstab`，在启动配额的磁盘挂载选项中添加`usrquota,grpquota`
2. 使用`mount -af`测试一下 fstab 有没有错误，如果有错的话系统将无法启动。
3. 安装quota: `apt install quota`
4. 创建配额文件: `quotacheck -amvug`
5. 编辑配额配置: `edquota -u user` or `edquota -g group`
6. 为其他用户复制`user`的配额信息： `for i in $(ls /home);do if [[ -d /home/$i ]];then echo quota $i;edquota -p user $i; fi;done`，其中`user`就是上一步修改过配额的用户
7. 重新挂载硬盘之后生效

## 报告配额使用状况
`repquota -as`

## 注意事项
- `edquota` 的时候数值的单位为kb