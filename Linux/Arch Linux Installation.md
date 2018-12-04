# 准备

1. 联网
2. `timedatectl set-ntp true`
3. `loadkeys dvorak`
4. `pacman -S tmux fish btrfs-progs`

# 分区

`mkfs.fat -F32 /dev/sdb1`

|  sd  | flags |   size   | mount point | file system |
| :--: | :---: | :------: | :---------: | :---------: |
| sdb1 |  efi  | 550 Mib  |    /boot    |    FAT32    |
| sdb2 |       | 94.8 Gib |      /      |    BTRFS    |
| sdb3 | swap  | 16.5 Gib |             |             |

# 挂载

```bash
mount /dev/sdb2 /mnt
cd /mnt

mkdir /mnt/boot /mnt/home

mount /dev/sdb1 /mnt/boot
mount /dev/sda2 /mnt/home
mkswap /dev/sdb3
swapon /dev/sdb3
```

# 安装配置基本系统

```bash
tmux
pacstrap /mnt base  # arch-install-scripts
genfstab -L /mnt >> /mnt/etc/fstab

arch-chroot /mnt
pacman -S intel-ucode
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
hwclock --systohc
# edit /etc/locale.gen
locale-gen
echo 'Laptop' > /etc/hostname
vim /etc/hosts
```

add below to `/etc/hosts`

```
# Static table lookup for hostnames.
# See hosts(5) for details.
127.0.0.1 localhost.localdomain localhost
#::1 localhost.localdomain localhost
127.0.0.1 license.sublimehq.com
127.0.0.1 45.55.255.55
127.0.0.1 45.55.41.223
```

```bash
useradd user
usermod user -aG adm
pacman -S sudo fish networkmanager
visudo
```

# 配置启动项

```bash
bootctl install
```

add to `/etc/pacman.d/hooks/systemd-boot.hook`

```toml
[Trigger]
Type=Package
Operation=Upgrade
Target=systemd

[Action]
Description=Updating sysdemd-boot
When=PostTransaction
Exec=/usr/bin/bootctl update
```

add to `/boot/loader/entries/archlinux.conf`

```
title Charles Xu's Arch Linux
linux /vmlinuz-linux
initrd /intel-ucode.img
initrd /initramfs-linux.img
options root=/dev/sdb2
options resume=/dev/sdb3
```

change `/etc/mkinitcpio.conf`

```
52:HOOKS=(base udev autodetect modconf block filesystems keyboard resume fsck)
```



#  安装后的配置

- 安装 git, fish-shell, tmux, curl, wget
- 安装 gnome
- 安装 [CharlesScripts](https://github.com/the0demiurge/CharlesScripts)
- 安装/删除软件 `inst (inst), yao (yao)`
- 开启相应服务

```
bluetooth
cronie
fail2ban
nmb
org.cups.cupsd
pkgfile-update.timer
preload
sshd
atd
gpm
wicd
#systemd-resolved
#systemd-networkd
```

- trizen powerline-console-fonts后，编辑`/etc/vconsole.conf`，加入`ter-powerline-v16n`
- `/etc/lightdm/lightdm-gtk-greeter.conf`

```toml
[greeter]
background = /home/charles/.cache/wallpaper/dialog-image.jpg
theme-name = Arc-Flatabulous-Dark
icon-theme-name = Papirus-Dark
screensaver-timeout = 10
```

