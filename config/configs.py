import os


def load_config():
    from dotenv import load_dotenv

    load_dotenv()

    config = {
        "API_BASE_URL": os.getenv("BASE_URL", "https://cloud-api.yandex.net/v1/disk"),
        "RESOURCE_ENDPOINT": os.getenv("RESOURCE_ENDPOINT", "resources"),
        "TRASH_ENDPOINT": os.getenv("TRASH_ENDPOINT", "trash/resources"),
        "OAUTH_TOKEN": os.getenv("OAUTH_TOKEN"),
    }

    if not config["OAUTH_TOKEN"]:
        raise ValueError("OAUTH_TOKEN environment variable is required")

    return config


config = load_config()

API_BASE_URL = config["API_BASE_URL"]
RESOURCE_ENDPOINT = config["RESOURCE_ENDPOINT"]
TRASH_ENDPOINT = config["TRASH_ENDPOINT"]
OAUTH_TOKEN = config["OAUTH_TOKEN"]
