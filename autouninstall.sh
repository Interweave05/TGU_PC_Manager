#!/bin/bash

set -e

# 判断 root 权限
if [[ $EUID -ne 0 ]]; then
  echo "❌ 请用 root 权限运行此脚本！"
  exit 1
fi

service_name="tgu_ubuntu_manager.service"
service_path="/etc/systemd/system/$service_name"
install_path="/opt/tgu_pc_manager"

echo "🔧 正在卸载 TGU Ubuntu Manager..."

# 停止并禁用 systemd 服务
if systemctl list-units --full -all | grep -Fq "$service_name"; then
  echo "停止服务 $service_name..."
  systemctl stop "$service_name" || true

  echo "禁用服务 $service_name..."
  systemctl disable "$service_name" || true
fi

# 删除 systemd 服务文件
if [ -f "$service_path" ]; then
  echo "删除 systemd 服务文件..."
  rm "$service_path"
else
  echo "未找到服务文件 $service_path，跳过。"
fi

# 重新加载 systemd 配置
echo "重新加载 systemd 配置..."
systemctl daemon-reload

# 删除程序目录
if [ -d "$install_path" ]; then
  echo "删除安装目录 $install_path..."
  rm -rf "$install_path"
else
  echo "未找到安装目录 $install_path，跳过。"
fi

echo "✅ 卸载完成。"

