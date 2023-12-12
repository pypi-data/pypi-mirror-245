"""
idnapi.cc.py
~~~~~~~~~~~~
Author: Mark Spain <Mark.Spain@ey.com>

Description:
This module implements the select CC endpoints of the IdentityNow REST API.
Note that the CC endpoints are not documented in the public API documentation and
are not supported by SailPoint. Use at your own risk. These endpoints are
subject to change without notice.
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

# remove an account from a record in IDN (does not provision downstream to the account source)
def idn_remove_account(params):
    print("idnapi.cc - idn_remove_account: enter function")

    config = params["config"]
    headers = params["headers"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/cc/api/account/remove/{params['id']}"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.cc - idn_remove_account: url: {url}")

    # invoke the api
    response = requests.delete(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.cc - idn_remove_account: response headers: {response.headers}")
        print(f"idnapi.cc - idn_remove_account: response body: {response.json()}")
    
    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.cc - idn_remove_account: problem removing account!")
        print("idnapi.cc - idn_remove_account: status code: ", response.status_code)
        print("idnapi.cc - idn_remove_account: reason: ", response.reason)
        print("idnapi.cc - idn_remove_account: text: ", response.text)
        raise Exception("idnapi.cc - idn_remove_account: problem removing account!")
    else:
        print("idnapi.cc - idn_remove_account: successfully removed account")
    
    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.cc - idn_remove_account: result: {result}")

    print("idnapi.cc - idn_remove_account: exit function")
    return result
