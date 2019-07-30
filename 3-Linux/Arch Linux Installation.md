# 准备

1. 联网
2. `timedatectl set-ntp true`
3. `loadkeys dvorak`
4. `pacman -S tmux fish btrfs-progs`

# 分区

`mkfs.fat -F32 /dev/sdb1`

|  sd  | flags |   size   |   mount point   | file system |
| :--: | :---: | :------: | :-------------: | :---------: |
| sda1 |       | 711 Gib  | /home/harddrive |    NTFS     |
| sda2 |       | 207 Gib  |      /home      |     XFS     |
| sda3 |       |  15 Gib  |      /var       |     XFS     |
| sdb1 |  efi  | 550 Mib  |      /boot      |    FAT32    |
| sdb2 |       | 94.8 Gib |        /        |    BTRFS    |
| sdb3 | swap  | 16.5 Gib |     [SWAP]      |    SWAP     |

# 挂载

```bash
cd /mnt
mount /dev/sdb2 /mnt

mkdir -p /mnt/boot /mnt/home /mnt/var

mount /dev/sdb1 /mnt/boot
mount /dev/sda2 /mnt/home
mount /dev/sda3 /mnt/var

mkdir -p /mnt/home/harddrive

mount /dev/sda1 /mnt/home/harddrive

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
```

```bash
useradd user
usermod user -aG adm
pacman -S sudo fish networkmanager
visudo
```

# 配置启动项

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

安装启动项

```bash
bootctl install
```

#  安装后的配置

- 安装 git, fish-shell, tmux, curl, wget

- 为了防止Btrfs格式文件系统损坏，设置`/etc/default/tlp`:

```
SATA_LINKPWR_ON_BAT=max_performance
```

- 安装 Xfce4

- 安装 [CharlesScripts](https://github.com/the0demiurge/CharlesScripts)

- 安装/删除软件 `inst (inst), yao (yao)`

- `timedatectl set-ntp true`

- 开启并配置相应服务（部分配置应参考[CharlesScripts](https://github.com/the0demiurge/CharlesScripts/tree/master/charles/installation.d/conf.d)中的自动配置脚本，比如tlp）

```
/etc/systemd/system
├── bluetooth.target.wants
│   └── bluetooth.service -> /usr/lib/systemd/system/bluetooth.service
├── dbus-fi.w1.wpa_supplicant1.service -> /usr/lib/systemd/system/wpa_supplicant.service
├── dbus-org.bluez.service -> /usr/lib/systemd/system/bluetooth.service
├── dbus-org.freedesktop.Avahi.service -> /usr/lib/systemd/system/avahi-daemon.service
├── dbus-org.freedesktop.NetworkManager.service -> /usr/lib/systemd/system/NetworkManager.service
├── dbus-org.freedesktop.nm-dispatcher.service -> /usr/lib/systemd/system/NetworkManager-dispatcher.service
├── dbus-org.freedesktop.resolve1.service -> /usr/lib/systemd/system/systemd-resolved.service
├── dbus-org.freedesktop.timesync1.service -> /usr/lib/systemd/system/systemd-timesyncd.service
├── display-manager.service -> /usr/lib/systemd/system/lightdm.service
├── getty.target.wants
│   └── getty@tty1.service -> /usr/lib/systemd/system/getty@.service
├── multi-user.target.wants
│   ├── atd.service -> /usr/lib/systemd/system/atd.service
│   ├── avahi-daemon.service -> /usr/lib/systemd/system/avahi-daemon.service
│   ├── avahi-dnsconfd.service -> /usr/lib/systemd/system/avahi-dnsconfd.service
│   ├── cronie.service -> /usr/lib/systemd/system/cronie.service
│   ├── dnscrypt-proxy.service -> /usr/lib/systemd/system/dnscrypt-proxy.service
│   ├── fail2ban.service -> /usr/lib/systemd/system/fail2ban.service
│   ├── gpm.service -> /usr/lib/systemd/system/gpm.service
│   ├── NetworkManager.service -> /usr/lib/systemd/system/NetworkManager.service
│   ├── org.cups.cupsd.path -> /usr/lib/systemd/system/org.cups.cupsd.path
│   ├── pkgfile-update.timer -> /usr/lib/systemd/system/pkgfile-update.timer
│   ├── remote-fs.target -> /usr/lib/systemd/system/remote-fs.target
│   ├── sshd.service -> /usr/lib/systemd/system/sshd.service
│   ├── systemd-resolved.service -> /usr/lib/systemd/system/systemd-resolved.service
│   ├── tlp.service -> /usr/lib/systemd/system/tlp.service
│   └── wpa_supplicant.service -> /usr/lib/systemd/system/wpa_supplicant.service
├── network-online.target.wants
│   └── NetworkManager-wait-online.service -> /usr/lib/systemd/system/NetworkManager-wait-online.service
├── printer.target.wants
│   └── org.cups.cupsd.service -> /usr/lib/systemd/system/org.cups.cupsd.service
├── sleep.target.wants
│   └── tlp-sleep.service -> /usr/lib/systemd/system/tlp-sleep.service
├── sockets.target.wants
│   ├── avahi-daemon.socket -> /usr/lib/systemd/system/avahi-daemon.socket
│   └── org.cups.cupsd.socket -> /usr/lib/systemd/system/org.cups.cupsd.socket
├── sysinit.target.wants
│   └── systemd-timesyncd.service -> /usr/lib/systemd/system/systemd-timesyncd.service
├── systemd-rfkill.service -> /dev/null
├── systemd-rfkill.socket -> /dev/null
└── timers.target.wants
    └── fstrim.timer -> /usr/lib/systemd/system/fstrim.timer

9 directories, 34 files
```

- trizen powerline-console-fonts后，编辑`/etc/vconsole.conf`，加入`ter-powerline-v16n`
- Add group users; Add $USER to `wheel, audio, users, realtime`
- `/etc/lightdm/lightdm-gtk-greeter.conf`

```toml
[greeter]
background = /home/charles/.cache/wallpaper/dialog-image.jpg
theme-name = Arc-Flatabulous-Dark
icon-theme-name = Papirus-Dark
screensaver-timeout = 10
```

- `/etc/polkit-1/rules.d/85-suspend.rules`

```
polkit.addRule(function(action, subject) {
    if (action.id == "org.freedesktop.login1.suspend" &&
        subject.isInGroup("users")) {
        return polkit.Result.YES;
    }
});
```

- `/etc/polkit-1/rules.d/86-mount.rules`

```
polkit.addRule(function(action, subject) {
    if (action.id == "org.freedesktop.udisks2.filesystem-mount-system" &&
        subject.isInGroup("users")) {
        return polkit.Result.YES;
    }
});
```
