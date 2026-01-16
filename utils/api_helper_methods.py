import allure

from config.configs import RESOURCE_ENDPOINT, TRASH_ENDPOINT
from models.models import TrashResponse
from utils.validator import response_validation


class FolderMethods:
    def __init__(self, client):
        self.folder_endpoint = RESOURCE_ENDPOINT
        self.trash_endpoint = TRASH_ENDPOINT
        self.api_client = client

    @allure.step("Установить авторизацию")
    def set_auth(self):
        self.api_client.set_auth()

    @allure.step("Снять авторизацию")
    def set_unauth(self):
        self.api_client.set_unauth()

    @allure.step("Получить список объектов в корзине")
    def get_trash_items(self, numb):
        params = {"limit": numb}
        response = self.api_client.get(self.trash_endpoint, params=params)
        data = response.json()
        return response_validation(data, TrashResponse)

    @allure.step("Получить данные папки")
    def get_folder(self, path):
        params = {"path": f"/{path}"}
        return self.api_client.get(self.folder_endpoint, params=params)

    @allure.step("Создать папку")
    def create_folder(self, path):
        params = {"path": f"/{path}"}
        return self.api_client.put(self.folder_endpoint, params=params)

    @allure.step("Удалить папку")
    def delete_folder(self, path):
        params = {"path": f"/{path}"}
        return self.api_client.delete(self.folder_endpoint, params=params)

    @allure.step("Очистить коризну")
    def clear_trash(self):
        self.api_client.delete(self.trash_endpoint)

    @allure.step("Восстановить папку")
    def restore_folder(self, path):
        trash_items = self.get_trash_items(10)["embedded"]["items"]
        for item in trash_items:
            if item["name"] == path:
                path = item["path"]
        params = {"path": path}
        restore_endpoint = f"{self.trash_endpoint}/restore"
        return self.api_client.put(restore_endpoint, params=params)
