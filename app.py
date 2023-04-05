from flask import Flask

from api.api_v1.endpoints.role import roles_router
from api.api_v1.endpoints.token import token_router
from api.api_v1.endpoints.users import users_router
from core.errors import HTTPException, http_exception_handler, general_exception_handler
from core.app_setup import sql_alchemy_teardown
from core.cors import setup_cors
from db.init_db import init_db

app = Flask(__name__)
init_db()
setup_cors(app)
# app.teardown_appcontext_funcs = [sql_alchemy_teardown]

for router in (users_router, token_router, roles_router):
    app.register_blueprint(router)

for error in (
    (HTTPException, http_exception_handler),
    (Exception, general_exception_handler),
):
    app.register_error_handler(error[0], error[1])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
