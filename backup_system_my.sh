#!/bin/bash
# set -o errexit

workdir=$(cd "$(dirname $0)" && pwd)
cd "$workdir"

######################################################
################## TODO: settings#####################
src_boot_device=/dev/sda1
src_root_device=/dev/sda2
src_boot_mount=/mnt/src/boot
src_root_mount=/mnt/src/root
dst_boot_device= # /dev/mapper/loop0p1
dst_root_device= # /dev/mapper/loop0p2
dst_boot_mount=/mnt/dst/boot
dst_root_mount=/mnt/dst/root
image_name=rasp.img
######################################################

green="\e[32;1m"
normal="\e[0m"

echo -e "${green}\n0.prepare:\n ${normal}"
[ -d $src_boot_mount ] && umount $src_boot_mount
[ -d $src_root_mount ] && umount $src_root_mount
[ -d $dst_boot_mount ] && umount $dst_boot_mount
[ -d $dst_root_mount ] && umount $dst_root_mount
[ ! -d $src_boot_mount ] && mkdir -p $src_boot_mount
[ ! -d $src_root_mount ] && mkdir -p $src_root_mount
[ ! -d $dst_boot_mount ] && mkdir -p $dst_boot_mount
[ ! -d $dst_root_mount ] && mkdir -p $dst_root_mount
last_loop_device=$(losetup -a | awk -F: '{print $1}')
[ "x${last_loop_device}" != "x" ] && losetup -d $last_loop_device
[ -f ./$image_name ] && rm -f ./$image_name

echo -e "${green}\n1.device settings:\n ${normal}"
echo -e "src_root_device: ${src_root_device}"
echo -e "src_boot_device: ${src_boot_device}"
read -p "Continue:" pause

mount -t vfat ${src_boot_device} ${src_boot_mount}
mount -t ext4 ${src_root_device} ${src_root_mount}

echo -e "${green}\n2.install software\n ${normal}"
sudo apt-get install -y dosfstools dump parted kpartx bc
# echo -e "${green} \ninstall software complete\n ${normal}"

echo -e "${green}\n3.create image now\n ${normal}"
boot_size=`df -P | grep $src_boot_device | awk '{print $3}'`
root_size=`df -P | grep $src_root_device | awk '{print $3}'`
if [ "x${root_size}" != "x" ] && [ "x${boot_size}" != "x" ];then
  count=`echo "${root_size}*1.1+${boot_size}+2"|bc|awk '{printf("%.0f",$1)}'`
else
  echo "device $src_root_device or $src_boot_device not exist,mount first"
  exit 0
fi
echo boot size:$boot_size,root_size:$root_size,block count: $count
# sudo dd if=/dev/zero of=$image_name bs=1k count=$count
# sudo parted $image_name --script -- mklabel msdos
# sudo parted $image_name --script -- mkpart primary fat32 1M $(($boot_size/1024+1))M
# sudo parted $image_name --script -- mkpart primary ext4 $(($root_size/1024+1))M -1

# allocate fixed disk size 8G
sudo dd if=/dev/zero of=$image_name bs=1024k count=$[1024*8]
sudo parted $image_name --script -- mklabel msdos
sudo parted $image_name --script -- mkpart primary fat32 1M 512M
sudo parted $image_name --script -- mkpart primary ext4 512M -1

echo -e "${green}4.mount loop device and copy files to image\n${normal}"
loopdevice=`sudo losetup --show -f $image_name`
echo "loopdevice:$loopdevice"
device=`sudo kpartx -va $loopdevice`
device=`echo $device | sed -E 's/.*(loop[0-9]*)p.*/\1/g' | head -1`
# device=`echo $device |awk '{print $3}' | head -1`
device="/dev/mapper/${device}"
dst_boot_device="${device}p1"
dst_root_device="${device}p2"
echo "dst_boot_device: ${dst_boot_device}"
echo "dst_root_device: ${dst_root_device}"
sleep 2
sudo mkfs.vfat $dst_boot_device
sudo mkfs.ext4 $dst_root_device

mount -t vfat $dst_boot_device ${dst_boot_mount}
mount -t ext4 $dst_root_device ${dst_root_mount}
echo -e "${green}copy /boot${normal}"
# sudo cp -rfp ${mount_path}/* /media/img_to
# sudo cp -rfp ${src_boot_mount}/* $dst_boot_mount
dd if=$src_boot_device of=$dst_boot_device

sudo chattr +d $image_name #exclude img file from backup(support in ext* file system)
echo "if 'Operation not supported while reading flags on $image_name' comes up, ignore it"

cd $dst_root_mount
echo -e "${green}copy /${normal}"
# sudo dump -0auf - /mnt/src/root/ | sudo restore -rf -
sudo dump -0auf - $src_root_mount | sudo restore -rf -

cd
sudo umount $src_boot_mount
sudo umount $src_root_mount
sudo umount $dst_boot_mount
sudo umount $dst_root_mount

sudo kpartx -d $loopdevice
sudo losetup -d $loopdevice

echo -e "${green}\nbackup complete\n${normal}"
