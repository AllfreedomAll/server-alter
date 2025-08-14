import xadmin
from apps.metrics.models import MetricsHistory

class MetricsHistoryAdmin:
    list_display = ['server', 'index_code', 'value', 'timestamp']
    list_filter = ['server', 'index_code', 'timestamp']
    search_fields = ['server__ip', 'server__name']

xadmin.site.register(MetricsHistory, MetricsHistoryAdmin)
