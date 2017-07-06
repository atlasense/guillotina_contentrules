from guillotina.testing import TESTING_SETTINGS
import pytest
from guillotina_contentrules.executor import Executor
from guillotina import app_settings


if 'applications' in TESTING_SETTINGS:
    TESTING_SETTINGS['applications'].append('guillotina_contentrules')
else:
    TESTING_SETTINGS['applications'] = ['guillotina_contentrules']


class TestExecutor(Executor):
    _records = {}


@pytest.fixture(scope='function')
def cr_executor():
    app_settings['contentrules_executor'] = TestExecutor
    TestExecutor._records.clear()
    yield TestExecutor
    TestExecutor._records.clear()
