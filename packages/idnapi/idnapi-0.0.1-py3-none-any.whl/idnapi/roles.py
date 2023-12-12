"""
idnapi.roles.py
~~~~~~~~~~~~~~~
Author: Mark Spain <Mark.Spain@ey.com>

Description:
This module implements the Roles endpoints of the IdentityNow REST API.
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

# search IDN for roles using the provided criteria (filters)
def idn_list_roles(params):
    print("idnapi.roles - idn_list_roles: enter function")

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
    url = f"https://{config['api_host']}/v3/roles?count={count}"
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
        print(f"idnapi.roles - idn_list_roles: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.roles - idn_list_roles: response headers: {response.headers}")
        print(f"idnapi.roles - idn_list_roles: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.roles - idn_list_roles: problem searching for roles!")
        print("idnapi.roles - idn_list_roles: status code: ", response.status_code)
        print("idnapi.roles - idn_list_roles: reason: ", response.reason)
        print("idnapi.roles - idn_list_roles: text: ", response.text)
        raise Exception("idnapi.roles - idn_list_roles: problem searching for roles!")
    else:
        print("idnapi.roles - idn_list_roles: successfully retrieved roles")

    # prepare result to return
    result = {
        "response": response.json()
    }
    if response.headers.get("X-Total-Count") is not None:
        result["count"] = int(response.headers["X-Total-Count"])

    print("idnapi.roles - idn_list_roles: exit function")
    return result


# get a role by id
def idn_get_role_by_id(params):
    print("idnapi.roles - idn_get_role_by_id: enter function")

    config = params["config"]
    headers = params["headers"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/roles/{params['id']}"

    if DEBUG_LOGGING:
        print(f"idnapi.roles - idn_get_role_by_id: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.roles - idn_get_role_by_id: response headers: {response.headers}")
        print(f"idnapi.roles - idn_get_role_by_id: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.roles - idn_get_role_by_id: problem retrieving role!")
        print("idnapi.roles - idn_get_role_by_id: status code: ", response.status_code)
        print("idnapi.roles - idn_get_role_by_id: reason: ", response.reason)
        print("idnapi.roles - idn_get_role_by_id: text: ", response.text)
        raise Exception("idnapi.roles - idn_get_role_by_id: problem retrieving role!")
    else:
        print("idnapi.roles - idn_get_role_by_id: successfully retrieved role")

    # prepare result to return
    result = {
        "response": response.json()
    }

    print("idnapi.roles - idn_get_role_by_id: exit function")
    return result
