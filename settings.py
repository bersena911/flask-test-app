import os
from functools import lru_cache

import dotenv

dotenv.load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT")
API_V1_STR = os.environ.get("API_V1_STR", "/api/v1")
SECRET_KEY = os.getenvb(b"SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)


@lru_cache()
def get_config() -> dict:
    """
    Returns secrets from secrets manager, if there is .env file overrides from it
    :return: secrets dict
    """
    config = {}
    config.update(os.environ)

    return config
