class OraenirException(Exception):
    """Critical exception with user-friendly context"""

    def __init__(self, message, errors=None, status_code=400):
        super().__init__(message)
        self.message = message
        self.errors = errors
        self.status_code = status_code

    def to_dict(self):
        error_dict = {'message': self.message}
        if self.errors:
            error_dict['errors'] = self.errors
        return error_dict