from guillotina import schema
from guillotina.async import IAsyncUtility
from zope.interface import Interface


class IContentRulesUtility(IAsyncUtility):
    pass


class IRule(Interface):
    conditions = schema.List()
    actions = schema.List()


class IConditionType(Interface):
    name = schema.TextLine()


class ICondition(Interface):
    condition_type = schema.TextLine()
    configuration = schema.JSONField()


class IActionType(Interface):
    name = schema.TextLine()


class IAction(Interface):
    action_type = schema.TextLine()
    configuration = schema.JSONField()


class IContentRuleSettings(Interface):
    rules = schema.JSONField()
