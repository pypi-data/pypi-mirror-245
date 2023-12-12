"""
idnapi.entitlements.py
~~~~~~~~~~~~~~~~~~~~~~
Author: Mark Spain <Mark.Spain@ey.com>

Description:
This module implements the Entitlements endpoints of the IdentityNow REST API.
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

# search IDN for entitlements using the provided criteria (filters)
def idn_list_entitlements(params):
    print("idnapi.entitlements - idn_list_entitlements: enter function")

    config = params["config"]
    headers = params["headers"]

    count = params["count"] if params.get("count") is not None else False
    limit = params.get("limit")
    offset = params.get("offset")
    filters = params.get("filters")
    sorters = params.get("sorters")

    # convert count (bool) to lowercase string
    count = str(count).lower()

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/beta/entitlements?count={count}"
    if limit is not None:
        url += f"&limit={limit}"
    if offset is not None:
        url += f"&offset={offset}"
    if filters is not None:
        url += f"&filters={filters}"
    if sorters is not None:
        url += f"&sorters={sorters}"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.entitlements - idn_list_entitlements: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.entitlements - idn_list_entitlements: response headers: {response.headers}")
        print(f"idnapi.entitlements - idn_list_entitlements: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.entitlements - idn_list_entitlements: problem searching for entitlements!")
        print("idnapi.entitlements - idn_list_entitlements: status code: ", response.status_code)
        print("idnapi.entitlements - idn_list_entitlements: reason: ", response.reason)
        print("idnapi.entitlements - idn_list_entitlements: text: ", response.text)
        raise Exception("idnapi.entitlements - idn_list_entitlements: problem searching for entitlements!")
    else:
        print("idnapi.entitlements - idn_list_entitlements: successfully retrieved entitlements")

    # prepare result to return
    result = {
        "response": response.json()
    }
    if response.headers.get("X-Total-Count") is not None:
        result["count"] = int(response.headers["X-Total-Count"])

    print("idnapi.entitlements - idn_list_entitlements: exit function")
    return result


# get a entitlement by id
def idn_get_entitlement_by_id(params):
    print("idnapi.entitlements - idn_get_entitlement_by_id: enter function")

    config = params["config"]
    headers = params["headers"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/beta/entitlements/{params['id']}"

    if DEBUG_LOGGING:
        print(f"idnapi.entitlements - idn_get_entitlement_by_id: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.entitlements - idn_get_entitlement_by_id: response headers: {response.headers}")
        print(f"idnapi.entitlements - idn_get_entitlement_by_id: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.entitlements - idn_get_entitlement_by_id: problem retrieving entitlement!")
        print("idnapi.entitlements - idn_get_entitlement_by_id: status code: ", response.status_code)
        print("idnapi.entitlements - idn_get_entitlement_by_id: reason: ", response.reason)
        print("idnapi.entitlements - idn_get_entitlement_by_id: text: ", response.text)
        raise Exception("idnapi.entitlements - idn_get_entitlement_by_id: problem retrieving entitlement!")
    else:
        print("idnapi.entitlements - idn_get_entitlement_by_id: successfully retrieved entitlement")

    # prepare result to return
    result = {
        "response": response.json()
    }

    print("idnapi.entitlements - idn_get_entitlement_by_id: exit function")
    return result
