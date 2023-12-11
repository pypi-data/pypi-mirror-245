import pytest
from apix.sync import SyncClient


@pytest.fixture
def client() -> SyncClient:
    return SyncClient()
