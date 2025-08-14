from rest_framework import serializers
from .models import Server, Threshold, AlertConfig


class ThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold
        fields = ['index_code', 'operator', 'value', 'enabled']


class AlertConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertConfig
        fields = ['alert_type', 'config', 'enabled']


class ServerSerializer(serializers.ModelSerializer):
    thresholds = ThresholdSerializer(many=True, read_only=True)
    alerts = AlertConfigSerializer(many=True, read_only=True)
    
    class Meta:
        model = Server
        fields = ['id', 'ip', 'name', 'thresholds', 'alerts', 'created_at', 'updated_at']


class ServerConfigSerializer(serializers.ModelSerializer):
    """用于TargetVPC获取配置的序列化器"""
    thresholds = serializers.SerializerMethodField()
    alerts = serializers.SerializerMethodField()
    
    class Meta:
        model = Server
        fields = ['ip', 'thresholds', 'alerts']
    
    def get_thresholds(self, obj):
        thresholds = Threshold.objects.filter(server=obj, enabled=True)
        return [
            {
                'index': t.index_code,
                'operator': t.operator,
                'value': float(t.value)
            }
            for t in thresholds
        ]
    
    def get_alerts(self, obj):
        alerts = AlertConfig.objects.filter(server=obj, enabled=True)
        return [
            {
                'type': a.alert_type,
                **a.config
            }
            for a in alerts
        ] 