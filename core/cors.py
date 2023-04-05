from flask_cors import CORS

from settings import get_config

config = get_config()


def setup_cors(app):
    origins = []
    # Set all CORS enabled origins
    if config.get("BACKEND_CORS_ORIGINS"):
        origins_raw = config.get("BACKEND_CORS_ORIGINS").split(",")
        for origin in origins_raw:
            use_origin = origin.strip()
            origins.append(use_origin)
    CORS(app, origins=origins, supports_credentials=True)
