import os
from dotenv import load_dotenv
from contextvars import ContextVar
import requests
import requests.api

load_dotenv()

API_URL = os.getenv("API_URL")

# Request-scoped JWT token context variable
request_token = ContextVar("request_token", default=None)

# Monkey patch requests to strip cookies and inject token as X-Auth header
original_request = requests.api.request

def patched_request(method, url, **kwargs):
    # Remove cookies from kwargs to prevent sending cookies
    kwargs.pop("cookies", None)
    
    if API_URL and url.startswith(API_URL):
        token = request_token.get()
        if token:
            headers = kwargs.get("headers", {})
            if headers is None:
                headers = {}
            else:
                headers = headers.copy()
            headers["X-Auth-Token"] = token
            headers["X-Auth-Header"] = token
            kwargs["headers"] = headers
            
    return original_request(method, url, **kwargs)

requests.request = patched_request
requests.api.request = patched_request


class ContextCookies(dict):
    def _get_current_dict(self):
        token = request_token.get()
        return {"token": token} if token is not None else {}

    def __getitem__(self, key):
        return self._get_current_dict()[key]

    def __setitem__(self, key, value):
        raise TypeError("ContextCookies is read-only")

    def __delitem__(self, key):
        raise TypeError("ContextCookies is read-only")

    def __contains__(self, key):
        return key in self._get_current_dict()

    def __iter__(self):
        return iter(self._get_current_dict())

    def __len__(self):
        return len(self._get_current_dict())

    def keys(self):
        return self._get_current_dict().keys()

    def values(self):
        return self._get_current_dict().values()

    def items(self):
        return self._get_current_dict().items()

    def get(self, key, default=None):
        return self._get_current_dict().get(key, default)

    def __str__(self):
        return str(self._get_current_dict())

    def __repr__(self):
        return repr(self._get_current_dict())

    def copy(self):
        return self._get_current_dict().copy()

cookies = ContextCookies()

MODELS = ["openai/gpt-oss-120b:free", "z-ai/glm-4.5-air:free"]

