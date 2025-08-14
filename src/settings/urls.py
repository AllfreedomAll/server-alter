"""lbseven URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home, name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import xadmin
from django.urls import include
from apps import urls as api_urls
from django.conf import settings


xadmin.autodiscover()
xadmin_url, xadmin_app, xadmin_ns = xadmin.site.urls

urlpatterns = [
    path("admin/", xadmin.site.urls),
    path('api/', include('apps.servers.urls')),
    path('api/', include('apps.metrics.urls')),
    path('api/', include('apps.alerts.urls')),
    
    # 直接添加metrics的URL，不使用api前缀
    path('metrics/', include('apps.metrics.urls')),
]


