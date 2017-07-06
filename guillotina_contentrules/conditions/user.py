from guillotina import configure, schema
from guillotina.utils import get_authenticated_user_id
from guillotina_contentrules.exceptions import ConfigurationError
from guillotina_contentrules.interfaces import IConditionType


class IPrincipalConditionType(IConditionType):
    user = schema.TextLine()


@configure.utility(provides=IPrincipalConditionType, name='principal')
def condition(ob, request, triggered_event, configuration):
    if 'user' not in configuration:
        raise ConfigurationError('No user provided in configuration')

    user = configuration['user']
    return get_authenticated_user_id(request) == user
