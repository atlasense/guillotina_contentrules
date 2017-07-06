from guillotina import schema
from guillotina.interfaces import (IObjectAddedEvent, IObjectModifiedEvent,
                                   IObjectRemovedEvent)
from guillotina_contentrules.interfaces import IConditionType
from guillotina_contentrules.exceptions import ConfigurationError


_event_types = {
    'add': IObjectAddedEvent,
    'modify': IObjectModifiedEvent,
    'remove': IObjectRemovedEvent
}


class IEventConditionType(IConditionType):
    event_name = schema.TextLine()


def condition(ob, triggered_event, configuration):
    if 'event_name' not in configuration:
        raise ConfigurationError('No event_name provided in configuration')

    event_name = configuration['event_name']
    if event_name not in _event_types:
        raise ConfigurationError(f'{event_name} is not a valid event_name')

    event_iface = _event_types[event_name]
    return event_iface.providedBy(triggered_event)
