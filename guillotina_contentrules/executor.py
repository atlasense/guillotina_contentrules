import logging

from guillotina import app_settings
from guillotina.utils import resolve_dotted_name

logger = logging.getLogger('guillotina_contentrules')


class Executor:

    def __init__(self, ob, event, rules):
        self._object = ob
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
                if condition_type not in app_settings['contentrules_conditions']:
                    logger.warn(f'Invalid configuration for condition, skipping: '
                                f'{condition_type}: {condition_configuration}')
                    break
                condition = resolve_dotted_name(
                    app_settings['contentrules_conditions'][condition_type])
                if condition(self._object, self._event, condition_configuration):
                    matched.append(rule)
                    break
        return matched

    async def execute_actions(self, rules):
        for rule in rules:
            for action in rule['actions']:
                action_type = action.get('action_type')
                action_configuration = action.get('configuration')
                if action_type not in app_settings['contentrules_actions']:
                    logger.warn(f'Invalid configuration for action, skipping: '
                                f'{action_type}: {rule_configuration}')
                    break
                action = resolve_dotted_name(
                    app_settings['contentrules_actions'][action_type])
                try:
                    action(self._object, self._event, action_configuration)
                except:
                    logger.warn('Error executing content rule action '
                                f'{action_type}: {rule_configuration}', exc_info=True)
