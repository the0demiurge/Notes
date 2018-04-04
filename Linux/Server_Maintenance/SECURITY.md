# 服务器安全指南

## 使用 Fail2Ban 保护 SSH 登录

本文摘抄自 [Linux 服务器安全简明指南](https://linux.cn/article-8076-1.html#3_4478)

[Fail2Ban](http://www.fail2ban.org/wiki/index.php/Main_Page) 是一个应用程序，它会在太多的失败登录尝试后禁止 IP 地址登录到你的服务器。由于合法登录通常不会超过三次尝试（如果使用 SSH 密钥，那不会超过一个），因此如果服务器充满了登录失败的请求那就表示有恶意访问。

Fail2Ban 可以监视各种协议，包括 SSH、HTTP 和 SMTP。默认情况下，Fail2Ban 仅监视 SSH，并且因为 SSH 守护程序通常配置为持续运行并监听来自任何远程 IP 地址的连接，所以对于任何服务器都是一种安全威慑。

有关安装和配置 Fail2Ban 的完整说明，请参阅我们的指南：[使用 Fail2ban 保护服务器](https://www.linode.com/docs/security/using-fail2ban-for-security)。

## 禁止Ping

- 临时禁止 Ping:

  `echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all`
- 永久禁止 Ping:

  1. 在 /etc/sysctl.conf 增加 `net.ipv4.icmp_echo_ignore_all=1`
  2. 或者在防火墙添加一条`iptables -A INPUT -p icmp --icmp-type 8 -s 0/0 -j DROP

防火墙允许 Ping:
```bash
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A OUTPUT -p icmp --icmp-type echo-reply -j ACCEPT
```