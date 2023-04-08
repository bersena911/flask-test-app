def validate_post_data(f):
    def decorated_function(*args, **kwargs):
        print(f.__annotations__)
        return f(*args, **kwargs)

    return decorated_function
