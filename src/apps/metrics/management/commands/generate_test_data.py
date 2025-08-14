from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from apps.servers.models import Server
from apps.metrics.models import MetricsHistory


class Command(BaseCommand):
    help = '生成测试用的指标数据（按分钟聚合）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='生成多少天的数据（默认7天）'
        )
        parser.add_argument(
            '--servers',
            type=int,
            default=3,
            help='生成多少个服务器的数据（默认3个）'
        )
        parser.add_argument(
            '--data-points-per-minute',
            type=int,
            default=5,
            help='每分钟生成多少个数据点（默认5个）'
        )

    def handle(self, *args, **options):
        days = options['days']
        num_servers = options['servers']
        data_points_per_minute = options['data_points_per_minute']
        
        self.stdout.write(f'开始生成{num_servers}个服务器{days}天的测试数据...')
        self.stdout.write(f'每分钟生成{data_points_per_minute}个数据点')
        
        # 确保有足够的服务器
        servers = list(Server.objects.all())
        if len(servers) < num_servers:
            self.stdout.write(f'现有服务器数量不足，创建{num_servers}个测试服务器...')
            for i in range(num_servers - len(servers)):
                server = Server.objects.create(
                    ip=f'192.168.1.{100 + i}',
                    name=f'测试服务器{i + 1}'
                )
                servers.append(server)
        
        # 指标代码列表
        index_codes = ['cpu_usage', 'memory_usage', 'disk_usage', 'network_io']
        
        # 生成数据
        end_time = timezone.now()
        start_time = end_time - timedelta(days=days)
        
        # 每分钟生成多个数据点
        current_time = start_time
        data_count = 0
        
        while current_time <= end_time:
            for server in servers[:num_servers]:
                for index_code in index_codes:
                    # 在每分钟内生成多个数据点
                    for i in range(data_points_per_minute):
                        # 计算当前分钟内的偏移时间（秒）
                        offset_seconds = random.randint(0, 59)
                        data_time = current_time + timedelta(seconds=offset_seconds)
                        
                        # 生成合理的随机值，添加一些趋势变化
                        base_value = self._get_base_value(index_code, data_time)
                        # 添加随机波动
                        variation = random.uniform(-5, 5)
                        value = max(0, min(100, base_value + variation))
                        
                        MetricsHistory.objects.create(
                            server=server,
                            index_code=index_code,
                            value=round(value, 2),
                            timestamp=data_time
                        )
                        data_count += 1
            
            current_time += timedelta(minutes=1)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'成功生成{data_count}条测试数据！\n'
                f'服务器数量: {num_servers}\n'
                f'时间范围: {start_time.strftime("%Y-%m-%d %H:%M")} 到 {end_time.strftime("%Y-%m-%d %H:%M")}\n'
                f'指标类型: {", ".join(index_codes)}\n'
                f'每分钟数据点: {data_points_per_minute}\n'
                f'数据密度: {data_points_per_minute * len(index_codes)} 个指标/分钟'
            )
        )
    
    def _get_base_value(self, index_code, time):
        """根据指标类型和时间生成基础值，模拟真实场景的变化趋势"""
        # 模拟一天内的变化趋势
        hour = time.hour
        
        if index_code == 'cpu_usage':
            # CPU使用率：工作时间较高，夜间较低
            if 8 <= hour <= 18:  # 工作时间
                base = 60 + (hour - 8) * 2  # 60% - 80%
            else:  # 夜间
                base = 20 + (hour - 0) * 1.5  # 20% - 35%
            return min(80, max(20, base))
            
        elif index_code == 'memory_usage':
            # 内存使用率：相对稳定，略有波动
            if 8 <= hour <= 18:
                base = 65 + (hour - 8) * 1.5  # 65% - 80%
            else:
                base = 50 + (hour - 0) * 1.2  # 50% - 65%
            return min(85, max(45, base))
            
        elif index_code == 'disk_usage':
            # 磁盘使用率：缓慢增长
            days_from_start = (time - timezone.now() + timedelta(days=7)).days
            base = 60 + abs(days_from_start) * 0.5  # 60% - 63.5%
            return min(90, max(55, base))
            
        else:  # network_io
            # 网络IO：工作时间活跃，夜间安静
            if 8 <= hour <= 18:
                base = 40 + (hour - 8) * 2  # 40% - 60%
            else:
                base = 15 + (hour - 0) * 1.5  # 15% - 30%
            return min(70, max(10, base)) 