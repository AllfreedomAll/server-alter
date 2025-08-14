from django.urls import path
from . import views

app_name = 'metrics'

urlpatterns = [
    path('chart/', views.metrics_chart_view, name='metrics_chart'),
    path('chart/echarts/', views.metrics_chart_echarts_view, name='metrics_chart_echarts'),
    path('test/', views.test_echarts_view, name='test_echarts'),
    path('data/', views.get_metrics_data, name='get_metrics_data'),
] 