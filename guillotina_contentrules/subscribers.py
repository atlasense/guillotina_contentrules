from guillotina import configure
from guillotina.component import getUtility
from guillotina.interfaces import (IObjectAddedEvent, IObjectModifiedEvent,
                                   IObjectRemovedEvent, IResource)
from guillotina.utils import get_current_request
from guillotina_contentrules.interfaces import IContentRulesUtility


@configure.subscriber(for_=(IResource, IObjectAddedEvent))
@configure.subscriber(for_=(IResource, IObjectModifiedEvent))
@configure.subscriber(for_=(IResource, IObjectRemovedEvent))
async def add_object(obj, event):
    utility = getUtility(IContentRulesUtility)
    await utility.push(obj, get_current_request(), event)
