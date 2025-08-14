from django.template.context import RequestContext
from xadmin.views.base import get_content_type_for_model
from django.utils.encoding import force_str as force_text, smart_str as smart_text
from xadmin.models import Log


def get_context_dict(context):
    """
     Contexts in django version 1.9+ must be dictionaries. As xadmin has a legacy with older versions of django,
    the function helps the transition by converting the [RequestContext] object to the dictionary when necessary.
    :param context: RequestContext
    :return: dict
    """
    if isinstance(context, RequestContext):
        ctx = context.flatten()
    else:
        ctx = context
    return ctx


def log(request, flag, message, obj=None):
    log = Log(
        user=request.user,
        ip_addr=request.META['REMOTE_ADDR'],
        action_flag=flag,
        message=message
    )
    if obj:
        log.content_type = get_content_type_for_model(obj)
        log.object_id = obj.pk
        log.object_repr = force_text(obj)
    log.save()
