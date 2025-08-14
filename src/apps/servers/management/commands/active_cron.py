import datetime
from datetime import timedelta

import httpx
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.metrics.models import MetricsHistory
from apps.servers.models import Server


def fetch_metrics_from_targetvpc():
    """从TargetVPC获取指标数据"""

    for server in Server.objects.all():
        try:
            print(f"开始获取server{server.ip}的数据")
            targetvpc_url = f"http://{server.ip}:8001"
            # 计算时间范围（前10分钟）
            end_time = timezone.now()
            start_time = end_time - timedelta(minutes=10)

            # 构建请求数据
            request_data = {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'indexes': ['cpu', 'memory', 'disk']
            }

            # 发送请求到TargetVPC
            with httpx.Client() as client:
                response = client.post(
                    f"{targetvpc_url}/api/metrics",
                    json=request_data,
                    headers={"X-Client-IP": server.ip}
                )

                if response.status_code == 200:
                    metrics_data = response.json()

                    # 处理指标数据
                    for metric_info in metrics_data:
                        index_code = metric_info['index']
                        values = metric_info['values']

                        if values:
                            # 计算平均值
                            bk_create = []
                            for v in values:
                                bk_create.append(MetricsHistory(
                                    server=server,
                                    index_code=index_code,
                                    value=v.get("v"),
                                    timestamp=datetime.datetime.fromtimestamp(v.get("ts"),tz=timezone.utc),

                                )
                                                 )
                            MetricsHistory.objects.bulk_create(bk_create)


                    print(f"成功获取服务器 {server.ip} 的指标数据")
                else:
                    print(f"获取服务器 {server.ip} 的指标数据失败: HTTP {response.status_code}")

        except Exception as e:
            print(f"获取服务器 {server.ip} 的指标数据失败: {e}")
            continue


def cleanup_old_metrics():
    """清理旧的指标数据（保留30天）"""
    cutoff_date = timezone.now() - timedelta(days=30)
    deleted_count = MetricsHistory.objects.filter(timestamp__lt=cutoff_date).delete()[0]
    print(f"清理了 {deleted_count} 条旧指标数据")

class Command(BaseCommand):
    '''每x分钟执行，拉取服务器的指标数据'''

    def handle(self, *args, **options):
        try:
            fetch_metrics_from_targetvpc()
            cleanup_old_metrics()

        except Exception as e:
            print(f"获取服务器数据失败")
            raise CommandError(e)
