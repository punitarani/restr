"""tests/conftest.py"""

import pytest

# Define fixtures
pytest_plugins = [
    "tests.fixtures.browser",
]


def pytest_configure(config):
    """Configure pytest"""

    config.addinivalue_line("markers", "order(int): run tests in a specific order")


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(session, config, items):
    """Modify test collection and items"""

    # Sort tests by order marker within same folder
    # Get folders (tests/folder/) and respective tests
    folders = {}
    for item in items:
        # item.module = tests/folder/test_file.py
        folder = item.module.__name__.split(".")[1]

        # Create folder if it doesn't exist
        if folder not in folders:
            folders[folder] = []

        # Add test to folder
        folders[folder].append(item)

    # Sort tests by order marker within same module
    for folder in folders:
        mod_vals = folders.get(folder)

        # Sort tests by order marker
        mod_vals.sort(
            key=lambda x: x.get_closest_marker("order").args[0]
            if x.get_closest_marker("order")
            else 10
        )

        # Replace folder with sorted tests
        folders[folder] = mod_vals

    # Replace items with sorted tests
    items[:] = [item for folder in folders for item in folders[folder]]

    # Print test order
    print("Test Order:")
    for item in items:
        print(item)
