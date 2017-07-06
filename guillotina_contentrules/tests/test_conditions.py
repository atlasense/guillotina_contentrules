import pytest
from guillotina.events import ObjectAddedEvent, ObjectRemovedEvent
from guillotina.tests.utils import create_content
from guillotina_contentrules.conditions import event
from guillotina_contentrules.exceptions import ConfigurationError


def test_event_condition_matches():
    ob = create_content()
    assert event.condition(ob, ObjectAddedEvent(ob), {
        'event_name': 'add'
    })


def test_event_condition_does_not_match():
    ob = create_content()
    assert not event.condition(ob, ObjectRemovedEvent(ob), {
        'event_name': 'add'
    })


def test_event_raises_configuration_error():
    ob = create_content()
    with pytest.raises(ConfigurationError):
        event.condition(ob, ObjectRemovedEvent(ob), {
            'event_name': 'foobar'
        })
