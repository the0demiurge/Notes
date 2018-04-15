```bash
#!/bin/bash
# 添加一个用户，并且记录加入的是谁
# 用法： adduser username 张三
sudo useradd $1 -s /bin/bash -m 
echo $1 $2 $(date) >> ~/.userscripts/.users
sudo cp ~/.userscripts/.users /root/.config
(echo 'password'
sleep 1
echo 'password')|sudo passwd $1 
echo "使用passwd改密码，初始密码为password"
sudo edquota -p $USER $1
sudo mkdir /data/
sudo echo 'export CUDA_VISIBLE_DEVICES=0'|tee -a /home/$1/.bashrc
```