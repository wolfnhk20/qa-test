import pytest

from database import reset_store


@pytest.fixture(autouse=True)
def clear_data_store():
    reset_store()
