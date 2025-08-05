#!/bin/bash

set -e

# 检查是否安装 sudo
if ! command -v sudo &> /dev/null; then
  echo "❌ 本脚本需要 sudo，但未安装 sudo。请先手动安装 sudo。"
  exit 1
fi

read -p "是否执行 apt update 和 upgrade？(y/n): " do_update
if [[ "$do_update" =~ ^[Yy]$ ]]; then
  echo "更新系统软件包..."
  sudo apt update && sudo apt upgrade -y
fi

# 安装 git
if ! command -v git &> /dev/null; then
  echo "检测到未安装 git，正在安装..."
  sudo apt install -y git
else
  echo "git 已安装"
fi

# 克隆仓库
repo_url="https://github.com/Interweave05/TGU_PC_Manager.git"
echo "将克隆 GitHub 仓库：$repo_url"

target_dir="/opt/tgu_pc_manager"

# 如果目录存在，先备份
if [ -d "$target_dir" ]; then
  echo "$target_dir 已存在，重命名为 ${target_dir}_backup_$(date +%s)"
  sudo mv "$target_dir" "${target_dir}_backup_$(date +%s)"
fi

echo "克隆仓库到 $target_dir ..."
sudo git clone "$repo_url" "$target_dir"

if [ $? -ne 0 ]; then
  echo "❌ 克隆仓库失败，退出安装。"
  exit 1
fi

# 安装 pip3
if ! command -v pip3 &> /dev/null; then
  echo "检测到未安装 pip3，正在安装..."
  sudo apt install -y python3-pip
else
  echo "pip3 已安装"
fi

# 安装 Python 依赖
if [ -f "$target_dir/requirements.txt" ]; then
  echo "安装 Python 依赖..."
  sudo pip3 install -r "$target_dir/requirements.txt"
else
  echo "❌ 未检测到 requirements.txt，退出安装。"
  exit 1
fi

# 复制 systemd 服务文件
service_src="$target_dir/tgu_pc_manager.service"
service_dst="/etc/systemd/system/tgu_ubuntu_manager.service"

if [ -f "$service_src" ]; then
  echo "复制 systemd 服务文件到 $service_dst ..."
  sudo cp "$service_src" "$service_dst"
else
  echo "未找到 $service_src，无法配置 systemd 服务。"
  exit 1
fi

echo "重新加载 systemd 配置..."
sudo systemctl daemon-reload

echo "启用并启动服务..."
sudo systemctl enable tgu_ubuntu_manager.service
sudo systemctl start tgu_ubuntu_manager.service

echo "服务状态："
sudo systemctl status tgu_ubuntu_manager.service --no-pager

echo "✅ 安装完成！"
