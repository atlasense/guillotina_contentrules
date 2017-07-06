import asyncio
import logging

from guillotina import configure
from guillotina.db.transaction import Status
from guillotina.transactions import get_tm, get_transaction
from guillotina_contentrules.executor import Executor
from guillotina_contentrules.interfaces import (IContentRuleSettings,
                                                IContentRulesUtility)

logger = logging.getLogger('guillotina_contentrules')


@configure.utility(provides=IContentRulesUtility)
class ContentRulesUtility:

    def __init__(self, settings=None, loop=None):
        self._loop = loop
        self._settings = {}
        self._conn = None
        self._pool = None

    async def initialize(self, app=None):
        self._queue = asyncio.Queue()

        while True:
            try:
                ob, request, event = await self._queue.get()
                txn = get_transaction(request)
                tm = get_tm(request)
                if txn is None or txn.status in (Status.ABORTED, Status.COMMITTED):
                    txn = await tm.begin(request)
                else:
                    # still finishing current transaction, this connection
                    # will be cut off, so we need to wait until we no longer
                    # have an active transaction on the reqeust...
                    await self.push(ob, request, event)
                    await asyncio.sleep(1)
                    continue

                try:
                    registry = self.request.container_settings
                    config = registry.for_interface(IContentRuleSettings)
                    if config is None:
                        continue

                    rules = [r for r in config['rules'].values()]
                    executor = Executor(ob, event, rules)
                    matching_rules = await executor.get_matching_rules()
                    await executor.execute_actions(matching_rules)
                    await tm.abort(txn=txn)
                except Exception as e:
                    logger.error(
                        "Exception executing content rules",
                        exc_info=e)
                    await tm.abort(txn=txn)
            except Exception:
                logger.warn(
                    'Error processing queue',
                    exc_info=True)
                await asyncio.sleep(1)
            finally:
                self._queue.task_done()

    async def finalize(self, app):
        pass

    async def push(self, ob, request, event):
        await self._queue.put((ob, request, event))
