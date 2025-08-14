#!/usr/bin/env bash

set -e  # 任何命令失败时退出


# 检测是否已安装 Docker
if command -v docker &> /dev/null; then
    echo " Docker 已安装，版本：$(docker --version)"
    exit 0
fi

# 检测系统类型
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo " 无法检测系统版本，请手动安装 Docker"
    exit 1
fi

echo "🔍 检测到系统：$OS"

# 根据系统类型安装 Docker
case "$OS" in
    ubuntu|debian)
        echo " 安装 Docker for $OS ..."
        apt-get update
        apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

        curl -fsSL https://download.docker.com/linux/$OS/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/$OS \
          $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

        apt-get update
        apt-get install -y docker-ce docker-ce-cli containerd.io
        ;;

    centos|rhel)
        echo " 安装 Docker for CentOS / RHEL ..."
        yum remove -y docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine || true
        yum install -y yum-utils
        yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        yum install -y docker-ce docker-ce-cli containerd.io
        ;;

    fedora)
        echo " 安装 Docker for Fedora ..."
        dnf -y remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine || true
        dnf -y install dnf-plugins-core
        dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
        dnf install -y docker-ce docker-ce-cli containerd.io
        ;;

    amzn)
        echo " 安装 Docker for Amazon Linux ..."
        amazon-linux-extras enable docker
        yum install -y docker
        ;;

    *)
        echo " 暂不支持自动安装的系统：$OS，请参考官方文档手动安装 Docker"
        exit 1
        ;;
esac

# 启动 Docker 并设置开机自启
systemctl enable docker
systemctl start docker

# 检查是否安装成功
if docker --version &> /dev/null; then
    echo " Docker 安装成功，版本：$(docker --version)"
else
    echo " Docker 安装失败"
    exit 1
fi

echo "🎉 Docker 安装完成！"