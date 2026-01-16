import pytest

from utils.api_client import APIClient
from utils.api_helper_methods import FolderMethods
from utils.test_data import generate_test_data


@pytest.fixture(scope="session")
def client():
    with APIClient() as api_client:
        yield api_client


@pytest.fixture
def folder_manager(client, unique_folder_name):
    fm = FolderMethods(client)
    fn = unique_folder_name
    result = {"methods": fm, "folder_name": fn}
    yield result
    fm.delete_folder(fn)


@pytest.fixture
def create_folder(client, unique_folder_name):
    fm = FolderMethods(client)
    fn = unique_folder_name
    response = fm.create_folder(fn)
    result = {"response": response, "folder_name": fn}
    yield result
    fm.delete_folder(fn)


@pytest.fixture
def unique_folder_name():
    return generate_test_data()


@pytest.fixture(scope="session", autouse=True)
def cleanup_trash_after_tests(client):
    yield
    fm = FolderMethods(client)
    fm.clear_trash()
