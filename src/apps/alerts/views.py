from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import AlertRecord
from apps.servers.models import Server


class AlertRecordViewSet(viewsets.ReadOnlyModelViewSet):
    """告警记录视图集"""
    queryset = AlertRecord.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = AlertRecord.objects.all()
        server_id = self.request.query_params.get('server_id')
        if server_id:
            queryset = queryset.filter(server_id=server_id)
        return queryset


@method_decorator(csrf_exempt, name='dispatch')
class AlertReportView(View):
    """告警上报视图 - 供TargetVPC调用"""
    
    def post(self, request):
        """接收告警上报"""
        try:
            import json
            data = json.loads(request.body)
            
            # 获取客户端IP
            client_ip = request.headers.get('X-Client-IP')
            if not client_ip:
                client_ip = request.META.get('REMOTE_ADDR')
            
            if not client_ip:
                return JsonResponse({'error': '无法获取客户端IP'}, status=400)
            
            # 查找服务器
            try:
                server = Server.objects.get(ip=client_ip)
            except Server.DoesNotExist:
                return JsonResponse({'error': '服务器未配置'}, status=404)
            
            # 创建告警记录
            AlertRecord.objects.create(
                server=server,
                index_code=data.get('index'),
                threshold_value=data.get('threshold'),
                current_value=data.get('current_value'),
                alert_type='unknown',  # 这里可以根据实际情况设置
                status='sent'
            )
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) 