from flask import g


def db_session_close():
    g.db_session.close()
