from utils.validator import response_validation


def assert_success_response(data, model):
    val_data = response_validation(data, model)
    assert "method" in val_data and val_data["method"] is not None, (
        "Missing 'method' field"
    )
    assert "href" in val_data and val_data["href"] is not None, "Missing 'href' field"
    assert "templated" in val_data and val_data["templated"] is not None, (
        "Missing 'templated' field"
    )


def assert_error_response(data, model):
    val_data = response_validation(data, model)
    assert "error" in val_data and val_data["error"] is not None, (
        "Missing 'error' field"
    )
    assert "description" in val_data and val_data["description"] is not None, (
        "Missing 'description' field"
    )
    assert "message" in val_data and val_data["message"] is not None, (
        "Missing 'message' field"
    )
