import pytest
from guillotina.events import ObjectAddedEvent, ObjectRemovedEvent
from guillotina.tests.utils import create_content, login
from guillotina_contentrules.conditions import event, user, type_name
from guillotina_contentrules.exceptions import ConfigurationError


def test_event_condition_matches(dummy_guillotina):
    ob = create_content()
    assert event.condition(ob, None, ObjectAddedEvent(ob), {
        'event_name': 'add'
    })


def test_event_condition_does_not_match(dummy_guillotina):
    ob = create_content()
    assert not event.condition(ob, None, ObjectRemovedEvent(ob), {
        'event_name': 'add'
    })


def test_event_raises_configuration_error(dummy_guillotina):
    ob = create_content()
    with pytest.raises(ConfigurationError):
        event.condition(ob, None, ObjectRemovedEvent(ob), {
            'event_name': 'foobar'
        })


def test_user_condition(dummy_request):
    login(dummy_request)
    ob = create_content()
    assert user.condition(ob, dummy_request, ObjectAddedEvent(ob), {
        'user': 'root'
    })

    assert not user.condition(ob, dummy_request, ObjectAddedEvent(ob), {
        'user': 'foobar'
    })


def test_type_name_condition(dummy_request):
    login(dummy_request)
    ob = create_content()
    assert type_name.condition(ob, dummy_request, ObjectAddedEvent(ob), {
        'type_name': 'Item'
    })

    assert not type_name.condition(ob, dummy_request, ObjectAddedEvent(ob), {
        'type_name': 'foobar'
    })
