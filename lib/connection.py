
import urllib3
import requests

# By default the Mozilla Cert list is used then return 'default'
# if disable-cert-verification is provided return 'none'
def getCertifcationSetting(ctx):
    if ctx.obj['disable-cert-verification']:
        # Since we are sending our own warning message disable the one from urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        print("InsecureRequestWarning: Unverified HTTPS request are being made. Disabling certificate verification is strongly discouraged.")
        return 'none'
    return 'default'


def requestWrap(ctx, method, url, *args, **kwargs):
    """
    Wraps requests.get/post/etc. calls to apply custom SSL certification settings.

    Args:
        method (str): The HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE').
        url (str): The URL for the request.
        *args: Positional arguments to pass to the requests method (rarely used, but included for completeness).
        **kwargs: Keyword arguments to pass to the requests method (e.g., params, data, json, headers, auth, timeout).

    Returns:
        requests.Response: The response object from the request.
    """
    
    certificateSetting = getCertifcationSetting(ctx)

    session = None # Initialize session outside of if/elif to potentially reuse

    if certificateSetting == 'default':
        # requests.get/post etc. by default use certifi and system CAs
        # No special session needed unless other common settings are applied
        pass 
    elif certificateSetting == 'none':
        # This disables SSL verification entirely. Use with extreme caution.
        kwargs['verify'] = False

    # Determine the requests method to call
    req_method = getattr(session if session else requests, method.lower())

    # Make the request
    response = req_method(url, *args, **kwargs)
    
    return response