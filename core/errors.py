from flask import jsonify


class HTTPException(Exception):
    def __init__(self, code: int, message: str):
        response = jsonify(message=message)
        response.status_code = code
        self.response = response


def http_exception_handler(e):
    return e.response


def general_exception_handler(e):
    print(e)
    return jsonify(message="Something Went Wrong"), 500


def bad_request_handler(e):
    return jsonify(message=e.description), 400
