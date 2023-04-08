from flask import Flask
from pydantic import ValidationError

from api.api_v1.endpoints.role import roles_router
from api.api_v1.endpoints.token import token_router
from api.api_v1.endpoints.users import users_router
from core.app_setup import db_session_close
from core.cors import setup_cors
from core.errors import (
    HTTPException,
    http_exception_handler,
    bad_request_handler,
    validation_error_handler,
)
from db.init_db import init_db

app = Flask(__name__)
init_db()
setup_cors(app)
app.after_request_funcs = [db_session_close]

for router in (users_router, token_router, roles_router):
    app.register_blueprint(router)

for error in (
    (HTTPException, http_exception_handler),
    (400, bad_request_handler),
    (ValidationError, validation_error_handler)
    # (Exception, general_exception_handler),
):
    app.register_error_handler(error[0], error[1])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
