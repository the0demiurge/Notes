# Linux 自动安装安全更新
摘抄自 [Linux 服务器安全简明指南](https://linux.cn/article-8076-1.html)

有一些用于服务器上自动更新的参数。[Fedora 的 Wiki](https://fedoraproject.org/wiki/AutoUpdates#Why_use_Automatic_updates.3F) 上有一篇很棒的剖析自动更新的利弊的文章，但是如果你把它限制到安全更新上，自动更新的风险将是最小的。

自动更新的可行性必须你自己判断，因为它归结为你在你的服务器上做什么。请记住，自动更新仅适用于来自仓库的包，而不是自行编译的程序。你可能会发现一个复制了生产服务器的测试环境是很有必要的。可以在部署到生产环境之前，在测试环境里面更新来检查问题。

- CentOS 使用 [yum-cron](https://fedoraproject.org/wiki/AutoUpdates#Fedora_21_or_earlier_versions) 进行自动更新。
- Debian 和 Ubuntu 使用 [无人值守升级](https://help.ubuntu.com/lts/serverguide/automatic-updates.html)。
- Fedora 使用 [dnf-automatic](https://dnf.readthedocs.org/en/latest/automatic.html)。
