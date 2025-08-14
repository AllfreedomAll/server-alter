from __future__ import absolute_import
import xadmin

from .models import UserSettings, Log
from xadmin import views
from django.utils.translation import gettext_lazy as _


class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True


xadmin.site.register(UserSettings, UserSettingsAdmin)


class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url(
                '%s_%s_change' % (instance.content_type.app_label, instance.content_type.model),
                instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''

    link.short_description = ""
    link.allow_tags = True
    link.is_column = False

    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    list_filter = ['action_time', ]
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'
    style_fields = {'user': "fk-ajax"}


xadmin.site.register(Log, LogAdmin)


class BaseSettings(object):
    enable_themes = True  # 使用主题功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSettings)


class GlobalSetting(object):
    # 设置base_site.html的Title
    # site_title = 'Space Fast'
    menu_style = "accordion"  # 菜单折叠

    # 设置base_site.html的Footer
    def get_site_menu(self):
        return []
        # menus_list = []
        # for i in PKG_INFO:
        #     menus_list.append(
        #         {
        #             'title': '%s' % i[1],
        #             'url': '/%sads/clientads/?_p_pkg__exact=%s' % (ADMIN_PATH, i[0]),
        #             'icon': ''
        #         },
        #
        #     )
        #
        # menus_list.append({
        #     'title': '广告位置',
        #     'url': '/%sads/adssite/' % (ADMIN_PATH),
        #     'icon': '', })
        # cus_menus = [
        #     {'title': 'Ads',
        #      'icon': 'fa-fw fa fa-cloud',
        #      'o': 2,
        #      'menus': menus_list,
        #      }
        #
        # ]
        # return cus_menus


xadmin.site.register(views.CommAdminView, GlobalSetting)
