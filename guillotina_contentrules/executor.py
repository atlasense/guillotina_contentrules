import logging

from guillotina.component import queryUtility
from guillotina_contentrules.interfaces import IConditionType, IActionType

logger = logging.getLogger('guillotina_contentrules')


class Executor:

    def __init__(self, ob, request, event, rules):
        self._object = ob
        self._request = request
        self._event = event
        self._rules = rules

    async def get_matching_rules(self):
        matched = []
        for rule in self._rules:
            if len(rule['conditions']) == 0:
                matched.append(rule)
                continue

            for condition in rule['conditions']:
                condition_type = condition.get('condition_type')
                condition_configuration = condition.get('configuration')
                condition = queryUtility(IConditionType, name=condition_type)
                if condition is None:
                    logger.warn(f'Invalid configuration for condition, skipping: '
                                f'{condition_type}: {condition_configuration}')
                    continue
                if condition(self._object, self._request, self._event,
                             condition_configuration):
                    matched.append(rule)
                    break
        return matched

    async def execute_actions(self, rules):
        for rule in rules:
            for action in rule['actions']:
                action_type = action.get('action_type')
                action_configuration = action.get('configuration')
                action = queryUtility(IActionType, name=action_type)
                if action is None:
                    logger.warn(f'Invalid configuration for action, skipping: '
                                f'{action_type}: {action_configuration}')
                    break
                try:
                    action(self._object, self._request,
                           self._event, action_configuration)
                except:
                    logger.warn('Error executing content rule action '
                                f'{action_type}: {action_configuration}',
                                exc_info=True)
