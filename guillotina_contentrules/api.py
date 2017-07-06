from guillotina import configure
from guillotina.interfaces import IContainer
from guillotina_contentrules.interfaces import IContentRuleSettings


def _get_rules(registry):
    config = registry.for_interface(IContentRuleSettings)
    if config is None:
        registry.register_interface(IContentRuleSettings)
        config = registry.for_interface(IContentRuleSettings)
        config['rules'] = {}
    return config


@configure.service(context=IContainer, method='GET', name='@content-rules',
                   permission='guillotina.ReadConfiguration')
async def get_contentrule(context, request):
    return _get_rules(request.container_settings)


@configure.service(context=IContainer, method='PATCH', name='@content-rules',
                   permission='guillotina.WriteConfiguration')
async def add_contentrule(context, request):
    registry = request.container_settings
    config = _get_rules(registry)
    rule = await request.json()
    config['rules'].update(rule)
    registry._p_register()
    return config


@configure.service(context=IContainer, method='DELETE', name='@content-rules',
                   permission='guillotina.WriteConfiguration')
async def remove_contentrule(context, request):
    registry = request.container_settings
    config = _get_rules(registry)
    data = await request.json()
    for rule_id in data['rules']:
        if rule_id in config['rules']:
            del config['rules'][rule_id]
    config._p_register()
    return config
