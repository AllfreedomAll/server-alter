from django.db import models
from django.contrib import admin


class Server(models.Model):
    """服务器模型"""
    ip = models.CharField(max_length=15, unique=True, verbose_name='IP地址')
    name = models.CharField(max_length=100, blank=True, verbose_name='服务器名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'
    
    def __str__(self):
        return f"{self.name} ({self.ip})"






class Threshold(models.Model):
    """阈值配置模型"""
    OPERATOR_CHOICES = [
        ('>', '大于'),
        ('>=', '大于等于'),
        ('<', '小于'),
        ('<=', '小于等于'),
    ]
    
    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name='服务器')
    index_code = models.CharField(max_length=20, verbose_name='指标代码')
    operator = models.CharField(max_length=10, choices=OPERATOR_CHOICES, verbose_name='操作符')
    value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='阈值')
    enabled = models.BooleanField(default=True, verbose_name='启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '阈值配置'
        verbose_name_plural = '阈值配置'
        unique_together = ['server', 'index_code']
    
    def __str__(self):
        return f"{self.server.ip} - {self.index_code} {self.operator} {self.value}%"


class AlertConfig(models.Model):
    """告警配置模型"""
    ALERT_TYPE_CHOICES = [
        ('email', '邮件'),
        ('feishu', '飞书'),
        ('dingtalk', '钉钉'),
    ]
    
    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name='服务器')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES, verbose_name='告警类型')
    config = models.JSONField(verbose_name='配置信息')
    enabled = models.BooleanField(default=True, verbose_name='启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '告警配置'
        verbose_name_plural = '告警配置'
    
    def __str__(self):
        return f"{self.server.ip} - {self.get_alert_type_display()}"


# Admin配置
