from django.urls import path, include
from . import views


urlpatterns = [
    path('alert-records/report/', views.AlertReportView.as_view(), name='alert-report'),
] 