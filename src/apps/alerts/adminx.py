import xadmin
from apps.alerts.models import AlertRecord

class AlertRecordAdmin:
    list_display = ['server', 'index_code', 'threshold_value', 'current_value', 'alert_type', 'status', 'created_at']
    list_filter = ['server', 'index_code', 'alert_type', 'status', 'created_at']
    search_fields = ['server__ip', 'server__name']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

xadmin.site.register(AlertRecord, AlertRecordAdmin)
