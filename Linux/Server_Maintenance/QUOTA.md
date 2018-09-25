# 磁盘配额设置

## 启动配额
1. 安装 quota: `apt install quota`
2. 编辑 `/etc/fstab`，在启动配额的磁盘挂载选项中添加`usrquota,grpquota`或`usrjquota=aquota.user,grpjquota=aquota.group,jqfmt=vfsv0`（如果内核支持和文件系统日志）
3. 使用`mount -afv`测试一下 fstab 有没有错误，如果有错的话系统将无法启动。
4. 重新挂载硬盘`mount -o remount,usrquota,grpquota sdX`
5. 创建配额文件: `quotacheck -amvugc`
6. 编辑一个配额配置: `edquota -u $user` or `edquota -g group`
7. 为其他用户复制`$user`的配额信息： `for i in $(ls /home);do if [[ -d /home/$i ]];then echo quota $i;edquota -p $user $i; fi;done`，其中`user`就是上一步修改过配额的用户

## 报告配额使用状况
`repquota -as`

## 注意事项
- `edquota` 的时候数值的单位为 kb

# 其他

`mount -o remount,rw`: 重新挂载