"""
idnapi.accessprofiles.py
~~~~~~~~~~~~~~~~~~~~~~~~
Author: Mark Spain <Mark.Spain@ey.com>

Description:
This module implements the Access Profiles endpoints of the IdentityNow REST API.
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

# search IDN for access profiles using the provided criteria (filters)
def idn_list_access_profiles(params):
    print("idnapi.accessprofiles - idn_list_access_profiles: enter function")

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
    url = f"https://{config['api_host']}/v3/access-profiles?count={count}"
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
        print(f"idnapi.accessprofiles - idn_list_access_profiles: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.accessprofiles - idn_list_access_profiles: response headers: {response.headers}")
        print(f"idnapi.accessprofiles - idn_list_access_profiles: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accessprofiles - idn_list_access_profiles: problem searching for access profiles!")
        print("idnapi.accessprofiles - idn_list_access_profiles: status code: ", response.status_code)
        print("idnapi.accessprofiles - idn_list_access_profiles: reason: ", response.reason)
        print("idnapi.accessprofiles - idn_list_access_profiles: text: ", response.text)
        raise Exception("idnapi.accessprofiles - idn_list_access_profiles: problem searching for access profiles!")
    else:
        print("idnapi.accessprofiles - idn_list_access_profiles: successfully retrieved access profiles")

    # prepare result to return
    result = {
        "response": response.json()
    }
    if response.headers.get("X-Total-Count") is not None:
        result["count"] = int(response.headers["X-Total-Count"])

    print("idnapi.accessprofiles - idn_list_access_profiles: exit function")
    return result


# get a access profile by id
def idn_get_access_profile_by_id(params):
    print("idnapi.accessprofiles - idn_get_access_profile_by_id: enter function")

    config = params["config"]
    headers = params["headers"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/access-profiles/{params['id']}"

    if DEBUG_LOGGING:
        print(f"idnapi.accessprofiles - idn_get_access_profile_by_id: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.accessprofiles - idn_get_access_profile_by_id: response headers: {response.headers}")
        print(f"idnapi.accessprofiles - idn_get_access_profile_by_id: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accessprofiles - idn_get_access_profile_by_id: problem retrieving access profile!")
        print("idnapi.accessprofiles - idn_get_access_profile_by_id: status code: ", response.status_code)
        print("idnapi.accessprofiles - idn_get_access_profile_by_id: reason: ", response.reason)
        print("idnapi.accessprofiles - idn_get_access_profile_by_id: text: ", response.text)
        raise Exception("idnapi.accessprofiles - idn_get_access_profile_by_id: problem retrieving access profile!")
    else:
        print("idnapi.accessprofiles - idn_get_access_profile_by_id: successfully retrieved access profile")

    # prepare result to return
    result = {
        "response": response.json()
    }

    print("idnapi.accessprofiles - idn_get_access_profile_by_id: exit function")
    return result
