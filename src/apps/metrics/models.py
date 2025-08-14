from django.db import models
from django.contrib import admin
from apps.servers.models import Server


class MetricsHistory(models.Model):
    """历史指标数据模型"""
    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name='服务器')
    index_code = models.CharField(max_length=20, verbose_name='指标代码')
    value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='指标值')
    timestamp = models.DateTimeField(verbose_name='时间戳')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '历史指标'
        verbose_name_plural = '历史指标'
        indexes = [
            models.Index(fields=['server', 'index_code', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.server.ip} - {self.index_code}: {self.value}% ({self.timestamp})"
