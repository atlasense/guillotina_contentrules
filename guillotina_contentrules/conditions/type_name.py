from guillotina import configure, schema
from guillotina_contentrules.exceptions import ConfigurationError
from guillotina_contentrules.interfaces import IConditionType


class ITypeNameConditionType(IConditionType):
    type_name = schema.TextLine()


@configure.utility(provides=ITypeNameConditionType, name='principal')
def condition(ob, request, triggered_event, configuration):
    if 'type_name' not in configuration:
        raise ConfigurationError('No type_name provided in configuration')

    type_name = configuration['type_name']
    return ob.type_name == type_name
