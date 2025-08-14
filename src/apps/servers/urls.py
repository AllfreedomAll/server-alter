from django.urls import path, include
from . import views



urlpatterns = [
    # API路由
    path('servers/config/', views.ServerConfigView.as_view(), name='server-config'),
    
    # 页面路由
    path('', views.server_dashboard, name='dashboard'),
    path('servers/<int:server_id>/', views.server_detail, name='server-detail'),
] 