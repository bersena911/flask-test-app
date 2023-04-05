from db.db_service import db_service


def sql_alchemy_teardown(app):
    db_service.dispose_engine()
