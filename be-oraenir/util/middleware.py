from flask import request
from functools import wraps

from .exception import OraenirException
from config import logger

def require_json_fields(required_fields: list[str]):
    """Validates the mandatory JSON fields"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == 'POST':
                if not request.is_json:
                    logger.warning('Received non-JSON header')
                    raise OraenirException('Must specify application/json')
                
                data = request.get_json(silent=True)

                if not data:
                    logger.warning('Received JSON header but invalid JSON')
                    raise OraenirException('Need a valid JSON body')
                
                missing_fields = []

                for field in required_fields:
                    if field not in data:
                        missing_fields.append(field)

                if missing_fields:
                    logger.warning(f'Missing mandatory JSON fields: {missing_fields}')
                    raise OraenirException(f'Missing mandatory fields: {missing_fields}')
                
            return func(*args, **kwargs)
        return wrapper
    return decorator