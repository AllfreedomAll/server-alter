import xadmin
from apps.servers.models import Server, Threshold, AlertConfig
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html


class ServerAdmin():
    list_display = ['ip', 'name', 'created_at', 'updated_at', 'view_chart_link']
    search_fields = ['ip', 'name']
    list_filter = ['created_at']
    
    def view_chart_link(self, obj):
        """显示查看图表的链接"""
        return format_html(
            '<a class="btn btn-xs btn-info" href="/metrics/chart/?server_id={}">'
            '<i class="fa fa-line-chart"></i> 查看图表</a>',
            obj.id
        )
    view_chart_link.short_description = "操作"
    view_chart_link.allow_tags = True
    
    def view_metrics_chart(self, request, queryset):
        """查看服务器指标图表"""
        if queryset.count() == 1:
            # 如果只选择了一个服务器，跳转到该服务器的图表页面
            server = queryset.first()
            return redirect(f'/metrics/chart/?server_id={server.id}')
        else:
            # 如果选择了多个服务器，跳转到通用图表页面
            server_ids = ','.join([str(s.id) for s in queryset])
            return redirect(f'/metrics/chart/?server_ids={server_ids}')
    
    view_metrics_chart.short_description = "查看指标图表"
    view_metrics_chart.icon = "fa-line-chart"
    
    actions = ['view_metrics_chart']


class ThresholdAdmin():
    list_display = ['server', 'index_code', 'operator', 'value', 'enabled']
    list_filter = ['server', 'index_code', 'operator', 'enabled']
    search_fields = ['server__ip', 'server__name']


class AlertConfigAdmin():
    list_display = ['server', 'alert_type', 'enabled', 'created_at']
    list_filter = ['server', 'alert_type', 'enabled']
    search_fields = ['server__ip', 'server__name']


xadmin.site.register(Server, ServerAdmin)
xadmin.site.register(Threshold, ThresholdAdmin)
xadmin.site.register(AlertConfig, AlertConfigAdmin)
