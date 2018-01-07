
def format_error_message(message, info, slug):
    return {
        'error_message': message,
        'error_info': info,
        'error_slug': slug,
    }


class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, slug="non-specific",
                 info=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.info = info
        self.slug = slug

    def to_dict(self):
        return format_error_message(self.message, self.info, self.slug)
