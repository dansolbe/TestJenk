import allure

from models.models import CreatedResponse, DI_ErrorResponse, DiskInfoResponse
from utils.assertion_helper import assert_error_response, assert_success_response
from utils.validator import response_validation


@allure.epic("Yandex Disc API тесты")
@allure.feature("Авторизация в API")
class Test_YaDisk_Auth:
    @allure.title("Авторизация с валидным токеном")
    @allure.step("Отправить GET запрос с авторизацией")
    def test_auth_with_valid_token(self, client):
        response = client.get()

        assert response.status_code == 200, (
            f"Request returns {response.status_code} code, expected 200"
        )
        data = response.json()
        val_data = response_validation(data, DiskInfoResponse)

        assert "user" in val_data and val_data["user"] is not None, (
            "Response body doesn't contain 'user' field"
        )
        assert "login" in val_data["user"] and val_data["user"]["login"] is not None, (
            "Response body doesn't contain 'login' field"
        )
        assert (
            "display_name" in val_data["user"]
            and val_data["user"]["display_name"] is not None
        ), "Response body doesn't contain 'display_name' field"

    @allure.title("Авторизация без токена")
    @allure.step("Отправить GET запрос без авторизации")
    def test_auth_without_token(self, client):
        client.set_unauth()
        response = client.get()

        assert response.status_code == 401, (
            f"Request returns {response.status_code} code, expected 401"
        )
        client.set_auth()
        data = response.json()
        val_data = response_validation(data, DI_ErrorResponse)

        assert "error" in val_data and val_data["error"] is not None, (
            "Error response body doesn't contain 'error' field"
        )
        assert "description" in val_data and val_data["description"] is not None, (
            "Error response body doesn't contain 'description' field"
        )
        assert "message" in val_data and val_data["message"] is not None, (
            "Error response body doesn't contain 'message' field"
        )


@allure.epic("Yandex Disc API тесты")
@allure.feature("Операции с папками")
class Test_YaDisk_Folders:
    @allure.title("Создать папку")
    def test_create_folder(self, folder_manager):
        methods, path = folder_manager["methods"], folder_manager["folder_name"]
        response = methods.create_folder(path)
        assert response.status_code == 201, (
            f"Request returns {response.status_code} code, expected 201"
        )
        data = response.json()
        assert_success_response(data, CreatedResponse)

    @allure.title("Создать папку без авторизации")
    def test_create_folder_noauth(self, folder_manager):
        methods, path = folder_manager["methods"], folder_manager["folder_name"]
        methods.set_unauth()
        response = methods.create_folder(path)
        assert response.status_code == 401, (
            f"Request returns {response.status_code} code, expected 401"
        )
        methods.set_auth()
        data = response.json()
        assert_error_response(data, DI_ErrorResponse)

    @allure.title("Создать папку по уже существующему пути")
    def test_create_existing_folder(self, folder_manager, create_folder):
        methods, path = folder_manager["methods"], create_folder["folder_name"]
        response = methods.create_folder(path)
        assert response.status_code == 409, (
            f"Request returns {response.status_code} code, expected 409"
        )
        data = response.json()
        assert_error_response(data, DI_ErrorResponse)

    @allure.title("Удалить папку")
    def test_delete_folder(self, folder_manager, create_folder):
        methods, path = folder_manager["methods"], create_folder["folder_name"]
        response = methods.delete_folder(path)
        assert response.status_code == 204, (
            f"Request returns {response.status_code} code, expected 204"
        )

    @allure.title("Удалить папку без авторизации")
    def test_delete_folder_unauth(self, folder_manager, create_folder):
        methods, path = folder_manager["methods"], create_folder["folder_name"]
        methods.set_unauth()
        response = methods.delete_folder(path)
        assert response.status_code == 401, (
            f"Request returns {response.status_code} code, expected 401"
        )
        methods.set_auth()
        data = response.json()
        assert_error_response(data, DI_ErrorResponse)

    @allure.title("Удалить несуществующую папку")
    def test_delete_folder_nonexist(self, folder_manager):
        methods, path = folder_manager["methods"], "NonExistentFolder"
        response = methods.delete_folder(path)
        assert response.status_code == 404, (
            f"Request returns {response.status_code} code, expected 404"
        )
        data = response.json()
        assert_error_response(data, DI_ErrorResponse)

    @allure.title("Восстановить удаленную папку")
    def test_restore_folder(self, folder_manager, create_folder):
        methods, path = folder_manager["methods"], create_folder["folder_name"]
        methods.delete_folder(path)
        response = methods.restore_folder(path)
        assert response.status_code == 201, (
            f"Request returns {response.status_code} code, expected 201"
        )
        data = response.json()
        assert_success_response(data, CreatedResponse)

    @allure.title("Восстановить несуществующую папку")
    def test_restore_folder_nonexist(self, folder_manager):
        methods, path = folder_manager["methods"], folder_manager["folder_name"]
        response = methods.restore_folder(path)
        assert response.status_code == 404, (
            f"Request returns {response.status_code} code, expected 404"
        )
        data = response.json()
        assert_error_response(data, DI_ErrorResponse)
