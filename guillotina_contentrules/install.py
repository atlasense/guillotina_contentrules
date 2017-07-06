# -*- coding: utf-8 -*-
from guillotina import configure
from guillotina.addons import Addon
from guillotina_contentrules.interfaces import IContentRuleSettings


@configure.addon(
    name="guillotina_contentrules",
    title="Provide dynamic actions based on content")
class ManageAddon(Addon):

    @classmethod
    def install(cls, container, request):
        registry = request.container_settings
        registry.register_interface(IContentRuleSettings)
        registry._p_register()

    @classmethod
    def uninstall(cls, container, request):
        registry = request.container_settings  # noqa
        # uninstall logic here...
