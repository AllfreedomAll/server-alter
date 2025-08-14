from rest_framework import serializers
from .models import MetricsHistory


class MetricsHistorySerializer(serializers.ModelSerializer):
    """指标历史数据序列化器"""
    server_name = serializers.CharField(source='server.name', read_only=True)
    server_ip = serializers.CharField(source='server.ip', read_only=True)
    
    class Meta:
        model = MetricsHistory
        fields = ['id', 'server', 'server_name', 'server_ip', 'index_code', 'value', 'timestamp', 'created_at']
        read_only_fields = ['created_at'] 