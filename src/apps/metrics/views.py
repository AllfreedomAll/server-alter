from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import MetricsHistory
from .serializers import MetricsHistorySerializer
from apps.servers.models import Server


class MetricsHistoryViewSet(viewsets.ModelViewSet):
    """指标历史数据视图集"""
    queryset = MetricsHistory.objects.all()
    serializer_class = MetricsHistorySerializer
    
    def get_queryset(self):
        queryset = MetricsHistory.objects.all()
        server_id = self.request.query_params.get('server_id', None)
        if server_id:
            queryset = queryset.filter(server_id=server_id)
        return queryset.order_by('-timestamp')


@api_view(['GET'])
def metrics_summary(request):
    """获取指标摘要"""
    return Response({
        'total_metrics': MetricsHistory.objects.count(),
        'message': 'Metrics API is working'
    }) 


def metrics_chart_view(request):
    """指标图表页面视图"""
    # 获取所有服务器
    servers = Server.objects.all()
    
    # 获取所有指标代码（从现有数据中提取）
    index_codes = MetricsHistory.objects.values_list('index_code', flat=True).distinct()
    
    # 获取默认日期范围（最近7天）
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    
    # 处理从servers传递过来的参数
    selected_server_ids = []
    if request.GET.get('server_id'):
        selected_server_ids = [request.GET.get('server_id')]
    elif request.GET.get('server_ids'):
        selected_server_ids = request.GET.get('server_ids').split(',')
    
    context = {
        'servers': servers,
        'index_codes': index_codes,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'selected_server_ids': selected_server_ids,
    }
    
    return render(request, 'metrics/metrics_chart.html', context)


def metrics_chart_echarts_view(request):
    """ECharts版本的指标图表页面视图"""
    # 获取所有服务器
    servers = Server.objects.all()
    
    # 获取所有指标代码（从现有数据中提取）
    index_codes = MetricsHistory.objects.values_list('index_code', flat=True).distinct()
    
    # 获取默认日期范围（最近7天）
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    
    # 处理从servers传递过来的参数
    selected_server_ids = []
    if request.GET.get('server_id'):
        selected_server_ids = [request.GET.get('server_id')]
    elif request.GET.get('server_ids'):
        selected_server_ids = request.GET.get('server_ids').split(',')
    
    context = {
        'servers': servers,
        'index_codes': index_codes,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'selected_server_ids': selected_server_ids,
    }
    
    return render(request, 'metrics/metrics_chart_echarts.html', context)


def test_echarts_view(request):
    """ECharts测试页面视图"""
    return render(request, 'metrics/test_echarts.html')


def get_metrics_data(request):
    """获取指标数据的API接口"""
    try:
        # 获取请求参数
        server_ids = request.GET.getlist('servers[]')
        index_codes = request.GET.getlist('index_codes[]')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        start_hour = request.GET.get('start_hour', '00')
        end_hour = request.GET.get('end_hour', '23')
        
        # 调试信息
        print(f"DEBUG: 接收到的参数 - server_ids: {server_ids}, index_codes: {index_codes}")
        print(f"DEBUG: 时间参数 - start_date: {start_date}, end_date: {end_date}, start_hour: {start_hour}, end_hour: {end_hour}")
        
        # 构建查询条件
        query = Q()
        
        if server_ids:
            query &= Q(server_id__in=server_ids)
        
        if index_codes:
            query &= Q(index_code__in=index_codes)
        
        if start_date:
            start_datetime = datetime.strptime(f"{start_date} {start_hour}:00:00", '%Y-%m-%d %H:%M:%S')
            query &= Q(timestamp__gte=start_datetime)
        
        if end_date:
            end_datetime = datetime.strptime(f"{end_date} {end_hour}:59:59", '%Y-%m-%d %H:%M:%S')
            query &= Q(timestamp__lte=end_datetime)
        
        # 查询数据
        metrics_data = MetricsHistory.objects.filter(query).select_related('server').order_by('timestamp')
        print(f"DEBUG: 查询到的数据条数: {metrics_data.count()}")
        print(f"DEBUG: 查询条件: {query}")
        
        # 数据聚合：按分钟聚合，取平均值
        aggregated_data = {}
        
        for metric in metrics_data:
            server_key = f"{metric.server.name or metric.server.ip}({metric.server.ip})"
            if server_key not in aggregated_data:
                aggregated_data[server_key] = {}
            
            if metric.index_code not in aggregated_data[server_key]:
                aggregated_data[server_key][metric.index_code] = {}
            
            # 将时间戳按分钟进行分组
            minute_key = metric.timestamp.strftime('%Y-%m-%d %H:%M')
            if minute_key not in aggregated_data[server_key][metric.index_code]:
                aggregated_data[server_key][metric.index_code][minute_key] = {
                    'values': [],
                    'count': 0
                }
            
            aggregated_data[server_key][metric.index_code][minute_key]['values'].append(float(metric.value))
            aggregated_data[server_key][metric.index_code][minute_key]['count'] += 1
        
        # 格式化聚合后的数据
        chart_data = {}
        all_timestamps = set()
        
        for server_key, server_data in aggregated_data.items():
            chart_data[server_key] = {}
            
            for index_code, index_data in server_data.items():
                chart_data[server_key][index_code] = {
                    'timestamps': [],
                    'values': []
                }
                
                # 按时间排序
                sorted_minutes = sorted(index_data.keys())
                
                for minute in sorted_minutes:
                    minute_data = index_data[minute]
                    # 计算平均值
                    avg_value = sum(minute_data['values']) / minute_data['count']
                    
                    chart_data[server_key][index_code]['timestamps'].append(minute + ':00')
                    chart_data[server_key][index_code]['values'].append(round(avg_value, 2))
                    
                    all_timestamps.add(minute + ':00')
        
        # 确保所有数据系列使用相同的时间轴
        sorted_timestamps = sorted(list(all_timestamps))
        
        # 重新格式化数据，确保时间轴一致
        for server_key in chart_data:
            for index_code in chart_data[server_key]:
                # 创建完整的时间轴数据
                complete_data = {}
                for timestamp in sorted_timestamps:
                    complete_data[timestamp] = None
                
                # 填充实际数据
                for i, timestamp in enumerate(chart_data[server_key][index_code]['timestamps']):
                    complete_data[timestamp] = chart_data[server_key][index_code]['values'][i]
                
                # 更新数据
                chart_data[server_key][index_code]['timestamps'] = sorted_timestamps
                chart_data[server_key][index_code]['values'] = [complete_data[ts] for ts in sorted_timestamps]
        
        return JsonResponse({
            'success': True,
            'data': chart_data,
            'timestamps': sorted_timestamps
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }) 