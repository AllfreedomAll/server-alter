from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Server
from .serializers import ServerSerializer, ServerConfigSerializer


class ServerViewSet(viewsets.ModelViewSet):
    """服务器视图集"""
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[])
    def config(self, request):
        """获取服务器配置 - 供TargetVPC调用"""
        client_ip = request.headers.get('X-Client-IP')
        if not client_ip:
            client_ip = request.META.get('REMOTE_ADDR')
        
        if not client_ip:
            return Response({'error': '无法获取客户端IP'}, status=400)
        
        try:
            server = Server.objects.get(ip=client_ip)
            serializer = ServerConfigSerializer(server)
            return Response(serializer.data)
        except Server.DoesNotExist:
            return Response({'error': '服务器未配置'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class ServerConfigView(View):
    """服务器配置视图 - 供TargetVPC调用"""
    
    def get(self, request):
        """获取服务器配置"""
        client_ip = request.headers.get('X-Client-IP')
        if not client_ip:
            client_ip = request.META.get('REMOTE_ADDR')
        
        if not client_ip:
            return JsonResponse({'error': '无法获取客户端IP'}, status=400)
        
        try:
            server = Server.objects.get(ip=client_ip)
            serializer = ServerConfigSerializer(server)
            return JsonResponse(serializer.data)
        except Server.DoesNotExist:
            return JsonResponse({'error': '服务器未配置'}, status=404)


def server_dashboard(request):
    """服务器仪表板"""
    servers = Server.objects.all()
    return render(request, 'servers/dashboard.html', {
        'servers': servers
    })


def server_detail(request, server_id):
    """服务器详情页面"""
    try:
        server = Server.objects.get(id=server_id)
        return render(request, 'servers/detail.html', {
            'server': server
        })
    except Server.DoesNotExist:
        return render(request, 'servers/404.html', status=404) 