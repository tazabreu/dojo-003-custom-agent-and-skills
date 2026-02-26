import pytest


def pytest_collection_modifyitems(config, items):
    for item in items:
        if "functional" in str(item.fspath):
            item.add_marker(pytest.marker.functional)
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.marker.unit)
