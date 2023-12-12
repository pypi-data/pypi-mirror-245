"""
idnapi.oauth.py
~~~~~~~~~~~~~~~
Author: Mark Spain <Mark.Spain@ey.com>

Description:
This module implements the OAuth functionality of the IdentityNow REST API,
specifically retrieving an OAuth token for use in other API calls.
"""
import requests
from requests.utils import requote_uri


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG_LOGGING = False


# ------------------------------------------------------------------------------
# Module
# ------------------------------------------------------------------------------

# get the oauth access token (authentication and authorization)
def idn_get_oauth_token(params):
    print("idnapi.oauth - idn_get_oauth_token: enter function")

    config = params["config"]
    headers = params["headers"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/oauth/token?grant_type=client_credentials&client_id={config['client_id']}&client_secret={config['client_secret']}"
    url = requote_uri(url)

    # invoke the api
    response = requests.post(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.oauth - idn_get_oauth_token: response headers: {response.headers}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.oauth - idn_get_oauth_token: problem obtaining oauth token!")
        print("idnapi.oauth - idn_get_oauth_token: status code: ", response.status_code)
        print("idnapi.oauth - idn_get_oauth_token: reason: ", response.reason)
        print("idnapi.oauth - idn_get_oauth_token: text: ", response.text)
        raise Exception("idnapi.oauth - idn_get_oauth_token: problem obtaining oauth token!")
    else:
        print("idnapi.oauth - idn_get_oauth_token: successfully obtained oauth token")

    # extract token to return
    token = response.json()["access_token"]

    print(f"idnapi.oauth - idn_get_oauth_token: exit function with return: REDACTED")
    return token
