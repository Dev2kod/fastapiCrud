import ssl
import urllib3
import requests


def bypassSsl():
    """
    Disables SSL verification globally for:
    - requests
    - urllib3
    - Python SSL context

    ⚠️ Use ONLY in development / restricted environments
    """

    # 1. Disable SSL verification in Python's SSL module
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except Exception:
        pass

    # 2. Disable warnings from urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # 3. Patch requests to ignore SSL verification by default
    original_request = requests.Session.request

    def patched_request(self, *args, **kwargs):
        kwargs['verify'] = False
        return original_request(self, *args, **kwargs)

    requests.Session.request = patched_request

    print("✅ SSL verification bypassed successfully")