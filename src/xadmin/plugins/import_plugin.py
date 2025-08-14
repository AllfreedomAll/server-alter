# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from xadmin.views import BaseAdminPlugin
from xadmin.plugins.utils import get_context_dict


class ImportMenuPlugin(BaseAdminPlugin):
    list_import = False

    def init_request(self, *args, **kwargs):
        return self.list_import

    def block_top_toolbar(self, context, nodes):
        context = get_context_dict(context or {})
        nodes.append(
            loader.render_to_string('xadmin/blocks/model_list.top_toolbar.import.html',
                                    context=context)
        )


class CheckConfPlugin(BaseAdminPlugin):
    check_conf = False

    def init_request(self, *args, **kwargs):
        return self.check_conf

    def block_top_toolbar(self, context, nodes):
        context = get_context_dict(context or {})
        nodes.append(
            loader.render_to_string('xadmin/blocks/model_list.top_toolbar.checkconf.html',
                                    context=context)
        )
