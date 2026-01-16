from typing import Any, Type, TypeVar

import allure
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@allure.step("Валидация/сериализация данных ответа")
def response_validation(data: dict[str, Any], model: Type[T]) -> dict[str, Any]:
    try:
        v_data = model.model_validate(data)
        return v_data.model_dump()
    except Exception as e:
        raise ValueError(f"Validation error: {e}")
