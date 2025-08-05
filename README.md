# TGU_PC_Manager

一款基于 Python Flask 的 Ubuntu 系统管理网页应用，帮助你通过网页方便地管理 Ubuntu 电脑。支持开机自启动管理（systemd）、磁盘空间监控、系统状态展示等功能，采用模块化设计，方便扩展。

---

## 功能与特点

- 🔄 **开机自启动管理**  
  使用 systemd 用户服务管理自启动程序，支持添加、启用、禁用和删除。

- 💾 **磁盘容量管理**  
  实时查看根目录各文件夹磁盘占用，支持清理 `/tmp` 临时文件目录。

- 🖥️ **系统信息展示**  
  显示 CPU、内存、硬盘基本状态，帮助快速了解系统健康。

- ⚡ **响应式网页设计**  
  采用 Bootstrap，界面简洁美观，支持移动端和桌面端。

- 🧱 **模块化结构**  
  各功能独立模块，方便后续维护和功能扩展。

---

## 依赖环境

- Ubuntu 22.04（其他版本未经验证）  
- Python 3.10（其他版本未经验证）  
- Flask ≥ 3.1.1  
- psutil ≥ 5.9.0

---

## 安装与运行

提供两种安装方式：一键安装脚本 或 手动安装

### 一、使用一键安装脚本

```bash
wget https://raw.githubusercontent.com/Interweave05/TGU_PC_Manager/refs/heads/main/autoinstall.sh 
sudo bash ./autoinstall.sh
```

或使用代理（使用下面的方法疑似会出现 sh 被篡改的问题）：

```bash
wget https://gh-proxy.com/https://raw.githubusercontent.com/Interweave05/TGU_PC_Manager/refs/heads/main/autoinstall.sh 
sudo bash ./autoinstall.sh
```

---

### 二、手动安装

> TODO

---

## 使用方式

使用浏览器（推荐 Firefox 或 Chrome）打开：

```
http://127.0.0.1:3040/
```

以访问管理界面。

---

## 卸载

```bash
wget https://raw.githubusercontent.com/Interweave05/TGU_PC_Manager/refs/heads/main/autouninstall.sh 
sudo bash ./autouninstall.sh
```

或使用代理（使用下面的方法疑似会出现 sh 被篡改的问题）：

```bash
wget https://gh-proxy.com/https://raw.githubusercontent.com/Interweave05/TGU_PC_Manager/refs/heads/main/autouninstall.sh 
sudo bash ./autouninstall.sh
```