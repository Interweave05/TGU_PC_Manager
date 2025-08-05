#!/bin/bash

set -e

# 判断 root 权限
if [[ $EUID -ne 0 ]]; then
  echo "请用 root 权限运行此脚本！"
  exit 1
fi

read -p "是否执行 apt update 和 upgrade？(y/n): " do_update
if [[ "$do_update" =~ ^[Yy]$ ]]; then
  echo "更新系统软件包..."
  apt update && apt upgrade -y
fi

# 安装 git
if ! command -v git &> /dev/null; then
  echo "检测到未安装 git，正在安装..."
  apt install -y git
else
  echo "git 已安装"
fi

# 克隆仓库
read -p "请输入你的 git 仓库地址: " repo_url
if [ -z "$repo_url" ]; then
  echo "仓库地址不能为空，退出。"
  exit 1
fi

# 目标路径
target_dir="/opt/tgu_pc_manager"

# 如果目录存在，先备份
if [ -d "$target_dir" ]; then
  echo "$target_dir 已存在，重命名为 ${target_dir}_backup_$(date +%s)"
  mv "$target_dir" "${target_dir}_backup_$(date +%s)"
fi

echo "克隆仓库到 $target_dir ..."
git clone "$repo_url" "$target_dir"

# 安装 python3-pip 如果没有
if ! command -v pip3 &> /dev/null; then
  echo "检测到未安装 pip3，正在安装..."
  apt install -y python3-pip
else
  echo "pip3 已安装"
fi

# 安装 Python 依赖
if [ -f "$target_dir/requirements.txt" ]; then
  echo "安装 Python 依赖..."
  pip3 install -r "$target_dir/requirements.txt"
else
  echo "未检测到 requirements.txt，跳过依赖安装。"
fi

# 复制 systemd 服务文件
service_src="$target_dir/tgu_pc_manager.service"
service_dst="/etc/systemd/system/tgu_ubuntu_manager.service"

if [ -f "$service_src" ]; then
  echo "复制 systemd 服务文件到 $service_dst ..."
  cp "$service_src" "$service_dst"
else
  echo "未找到 $service_src，无法配置 systemd 服务。"
  exit 1
fi

echo "重新加载 systemd 配置..."
systemctl daemon-reload

echo "启用并启动服务..."
systemctl enable tgu_ubuntu_manager.service
systemctl start tgu_ubuntu_manager.service

echo "服务状态："
systemctl status tgu_ubuntu_manager.service --no-pager

echo "安装完成！"
