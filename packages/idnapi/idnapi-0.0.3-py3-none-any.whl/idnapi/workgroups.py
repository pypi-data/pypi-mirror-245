"""
idnapi.workgroups.py
~~~~~~~~~~~~~~~~~~~~
Author: Mark Spain <Mark.Spain@ey.com>

Description:
This module implements the Governance Groups endpoints of the IdentityNow REST API.
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

# search IDN for governance groups (workgroups) using the provided criteria (filters)
def idn_list_governance_groups(params):
    print("idnapi.workgroups - idn_list_governance_groups: enter function")

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
    url = f"https://{config['api_host']}/beta/workgroups?count={count}"
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
        print(f"idnapi.workgroups - idn_list_governance_groups: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.workgroups - idn_list_governance_groups: response headers: {response.headers}")
        print(f"idnapi.workgroups - idn_list_governance_groups: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.workgroups - idn_list_governance_groups: problem searching for governance groups!")
        print("idnapi.workgroups - idn_list_governance_groups: status code: ", response.status_code)
        print("idnapi.workgroups - idn_list_governance_groups: reason: ", response.reason)
        print("idnapi.workgroups - idn_list_governance_groups: text: ", response.text)
        raise Exception("idnapi.workgroups - idn_list_governance_groups: problem performing search query!")
    else:
        print("idnapi.workgroups - idn_list_governance_groups: successfully searched for governance groups")

    # prepare result to return
    result = {
        "response": response.json()
    }
    if response.headers.get("X-Total-Count") is not None:
        result["count"] = int(response.headers["X-Total-Count"])

    if DEBUG_LOGGING:
        print(f"idnapi.workgroups - idn_list_governance_groups: result: {result}")

    print("idnapi.workgroups - idn_list_governance_groups: exit function")
    return result


# get a governance group (workgroup) by id
def idn_get_governance_group_by_id(params):
    print("idnapi.workgroups - idn_get_governance_group_by_id: enter function")

    config = params["config"]
    headers = params["headers"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/beta/workgroups/{params['id']}"

    if DEBUG_LOGGING:
        print(f"idnapi.workgroups - idn_get_governance_group_by_id: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.workgroups - idn_get_governance_group_by_id: response headers: {response.headers}")
        print(f"idnapi.workgroups - idn_get_governance_group_by_id: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.workgroups - idn_get_governance_group_by_id: problem getting governance group!")
        print("idnapi.workgroups - idn_get_governance_group_by_id: status code: ", response.status_code)
        print("idnapi.workgroups - idn_get_governance_group_by_id: reason: ", response.reason)
        print("idnapi.workgroups - idn_get_governance_group_by_id: text: ", response.text)
        raise Exception("idnapi.workgroups - idn_get_governance_group_by_id: problem getting governance group!")
    else:
        print("idnapi.workgroups - idn_get_governance_group_by_id: successfully got governance group")

    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.workgroups - idn_get_governance_group_by_id: result: {result}")

    print("idnapi.workgroups - idn_get_governance_group_by_id: exit function")
    return result


# list governance group members by governance group id
def idn_list_governance_group_members(params):
    print("idnapi.workgroups - idn_list_governance_group_members: enter function")

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
    url = f"https://{config['api_host']}/beta/workgroups/{params['id']}/members?count={count}"
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
        print(f"idnapi.workgroups - idn_list_governance_group_members: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.workgroups - idn_list_governance_group_members: response headers: {response.headers}")
        print(f"idnapi.workgroups - idn_list_governance_group_members: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.workgroups - idn_list_governance_group_members: problem listing governance group members!")
        print("idnapi.workgroups - idn_list_governance_group_members: status code: ", response.status_code)
        print("idnapi.workgroups - idn_list_governance_group_members: reason: ", response.reason)
        print("idnapi.workgroups - idn_list_governance_group_members: text: ", response.text)
        raise Exception("idnapi.workgroups - idn_list_governance_group_members: problem listing governance group members!")
    else:
        print("idnapi.workgroups - idn_list_governance_group_members: successfully listed governance group members")

    # prepare result to return
    result = {
        "response": response.json()
    }
    if response.headers.get("X-Total-Count") is not None:
        result["count"] = int(response.headers["X-Total-Count"])

    if DEBUG_LOGGING:
        print(f"idnapi.workgroups - idn_list_governance_group_members: result: {result}")

    print("idnapi.workgroups - idn_list_governance_group_members: exit function")
    return result
