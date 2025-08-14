# 🖥️ Server-Alter 服务器监控系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个基于Django + xadmin的现代化服务器监控管理系统，提供实时指标监控、告警管理、可视化图表等功能。

## ✨ 功能特性

### 🖥️ 服务器管理
- **服务器信息管理**: IP地址、名称、创建时间等基础信息
- **批量操作**: 支持批量选择服务器进行操作
- **状态监控**: 实时监控服务器运行状态

### 📊 指标监控
- **多指标支持**: CPU、内存、磁盘、网络等性能指标
- **历史数据**: 按分钟聚合的历史指标数据存储
- **数据可视化**: 支持Bootstrap和ECharts两种图表展示方式
- **灵活筛选**: 支持按服务器、指标、时间范围进行数据筛选

### 🚨 告警系统
- **阈值配置**: 为每个服务器的每个指标设置告警阈值
- **多渠道告警**: 支持邮件、飞书、钉钉等多种告警方式
- **告警记录**: 完整的告警历史记录和状态跟踪
- **实时上报**: 支持TargetVPC实时上报告警信息

### 🎨 管理界面
- **xadmin集成**: 基于xadmin的现代化管理界面
- **响应式设计**: 支持桌面端和移动端访问
- **权限管理**: 完整的用户权限控制系统

## 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   TargetVPC     │    │   Django App    │    │   Database      │
│   (监控代理)     │◄──►│   (监控系统)     │◄──►│   (数据存储)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   指标收集      │    │   数据处理      │    │   数据展示      │
│   告警上报      │    │   聚合计算      │    │   图表渲染      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+
- **Django**: 4.0+
- **数据库**: SQLite (开发) / MySQL/PostgreSQL (生产)
- **操作系统**: Linux, macOS, Windows

### 本地安装步骤

1. **克隆项目**
```bash
git clone https://github.com/AllfreedomAll/server-alter.git
cd server-alter
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **数据库迁移**
```bash
cd src
python manage.py makemigrations
python manage.py migrate
```

5. **创建超级用户**
```bash
python manage.py createsuperuser
```

6. **启动服务**
```bash
python manage.py runserver localhost:8000
```

### 访问地址

- **管理后台**: http://localhost:8000/admin/
- **指标图表**: http://localhost:8000/metrics/chart/
- **ECharts图表**: http://localhost:8000/metrics/chart/echarts/

## 📖 使用指南

### 1. 服务器管理

1. 登录管理后台
2. 进入"服务器"模块
3. 添加新服务器，填写IP地址和名称
4. 配置告警阈值和告警方式

### 2. 指标监控

1. 在服务器列表中选择要查看的服务器
2. 点击"查看指标图表"操作
3. 选择指标类型和时间范围
4. 查看历史趋势图表

### 3. 告警配置

1. 在"阈值配置"模块设置告警阈值
2. 在"告警配置"模块配置告警方式
3. 系统自动监控并触发告警

### 4. 图表展示

系统提供两种图表展示方式：

- **Bootstrap版本**: 轻量级，兼容性好
- **ECharts版本**: 美观，功能丰富，支持交互

## 🔧 配置说明

### 环境变量

```bash
# 数据库配置
DATABASE_URL=mysql://user:pass@localhost/dbname

# 告警配置
ALERT_EMAIL_HOST=smtp.gmail.com
ALERT_EMAIL_PORT=587
ALERT_EMAIL_USER=your-email@gmail.com
ALERT_EMAIL_PASSWORD=your-password

# 飞书配置
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx

# 钉钉配置
DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=xxx
```

### 定时任务

系统使用uWSGI定时任务进行数据收集：

```bash
# 启动定时任务
uwsgi --ini config/uwsgi.prod.ini

# 开发环境
python manage.py runserver
```

## 📊 数据模型

### 核心实体

- **Server**: 服务器信息
- **MetricsHistory**: 历史指标数据
- **Threshold**: 告警阈值配置
- **AlertConfig**: 告警方式配置
- **AlertRecord**: 告警记录

### 数据关系

```
Server (1) ── (N) MetricsHistory
Server (1) ── (N) Threshold
Server (1) ── (N) AlertConfig
Server (1) ── (N) AlertRecord
```

## 🌐 API接口

系统提供完整的RESTful API接口：

- **服务器配置**: `GET /api/servers/config/`
- **指标数据**: `GET /metrics/data/`
- **告警上报**: `POST /api/alert-records/report/`

详细API文档请参考 [API_SPEC.md](API_SPEC.md)

## 🧪 测试数据

### 生成测试数据

```bash
# 生成服务器数据
python manage.py shell
>>> from apps.servers.models import Server
>>> Server.objects.create(ip='192.168.1.100', name='测试服务器')

# 生成指标数据
python manage.py generate_test_data --servers 5 --days 7 --data-points-per-minute 3
```

### 测试命令

```bash
# 检查系统状态
python manage.py check

# 运行测试
python manage.py test

# 收集静态文件
python manage.py collectstatic
```

## 🚀 部署指南

### 生产环境部署

1. **使用uWSGI**
```bash
uwsgi --ini config/uwsgi.prod.ini
```

2. **使用Docker**
```bash
docker build -t server-alter .
docker run -p 8000:8000 server-alter
```

3. **使用Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 部署脚本

项目提供了便捷的部署脚本：

```bash
# 生产环境部署
./deploy_prod.sh

# 测试环境部署
./deploy_stage.sh
```

## 🔍 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务状态
   - 验证连接参数
   - 确认数据库权限

2. **图表显示异常**
   - 检查浏览器控制台错误
   - 验证数据接口返回
   - 确认JavaScript库加载

3. **告警发送失败**
   - 检查网络连接
   - 验证告警配置
   - 查看系统日志

### 日志查看

```bash
# 查看应用日志
tail -f logs/apps.log

# 查看命令日志
tail -f logs/command.log

# 查看下载日志
tail -f logs/download_info.log
```

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 更新日志

### v1.0.0 (2024-01-01)
- ✨ 初始版本发布
- 🖥️ 基础服务器管理功能
- 📊 指标监控和图表展示
- 🚨 告警系统和多渠道通知
- 🎨 xadmin管理界面集成

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- **项目维护者**: guo.ling
- **邮箱**: guo.ling@outlook.com
- **项目地址**: https://github.com/AllfreedomAll/server-alter
- **问题反馈**: https://github.com/AllfreedomAll/server-alter/issues

## 🙏 致谢

感谢以下开源项目的支持：

- [Django](https://www.djangoproject.com/) - Web框架
- [xadmin](https://github.com/sshwsfc/xadmin) - 管理界面
- [ECharts](https://echarts.apache.org/) - 图表库
- [Bootstrap](https://getbootstrap.com/) - UI框架

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
