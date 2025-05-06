import re
import ipaddress

from urllib.parse import urlparse
from random import choices

ascii = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{4,50}$')

def is_private_ip(ip_string: str) -> bool:
    if not isinstance(ip_string, str):
        return False
        
    try:
        ip_obj = ipaddress.ip_address(ip_string)

        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_multicast:
            return True

        return False
    except ValueError:
        return False

def is_valid_url(url: str) -> bool:
    if not isinstance(url, str):
        return False

    allowed_schemes = ['http', 'https']

    try:
        result = urlparse(url)

        if not all([result.scheme, result.netloc]):
            return False

        if result.scheme.lower() not in allowed_schemes:
            return False
        
        if is_private_ip(result.hostname):
            return False

        return True

    except ValueError:
        return False
    
    except Exception:
        return False

def is_valid_url_id(id: str) -> bool:
    if not isinstance(id, str):
        return False
    
    return bool(ID_PATTERN.match(id))

def get_random_string(n: int):
    return ''.join(choices(ascii, k=n))