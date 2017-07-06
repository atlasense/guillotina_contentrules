from guillotina.tests.utils import create_content
from guillotina.events import ObjectAddedEvent


async def test_executes_actions(dummy_guillotina, cr_executor):
    ob = create_content()
    executor = cr_executor(ob, None, ObjectAddedEvent(ob), [{
        'conditions': [{
            'condition_type': 'event',
            'configuration': {
                'event_name': 'add'
            }
        }]
    }])

    assert len(await executor.get_matching_rules()) == 1
