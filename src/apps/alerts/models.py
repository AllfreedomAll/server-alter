from django.db import models
from django.contrib import admin
from apps.servers.models import Server


class AlertRecord(models.Model):
    """告警记录模型"""
    STATUS_CHOICES = [
        ('sent', '已发送'),
        ('failed', '发送失败'),
    ]
    
    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name='服务器')
    index_code = models.CharField(max_length=20, verbose_name='指标代码')
    threshold_value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='阈值')
    current_value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='当前值')
    alert_type = models.CharField(max_length=20, verbose_name='告警类型')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '告警记录'
        verbose_name_plural = '告警记录'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.server.ip} - {self.index_code}: {self.current_value}% > {self.threshold_value}%"


