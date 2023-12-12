"""
idnapi.search.py
~~~~~~~~~~~~~~~~
Author: Mark Spain <Mark.Spain@ey.com>

Description:
This module implements the search functionality of the IdentityNow REST API.
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

# search IDN for objects using the provided search criteria (data)
def idn_search(params):
    print("idnapi.search - idn_search: enter function")

    config = params["config"]
    headers = params["headers"]
    data = params["data"]

    count = params["count"] if params.get("count") is not None else False
    limit = params.get("limit")
    offset = params.get("offset")

    # convert count (bool) to lowercase string
    count = str(count).lower()

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/search?count={count}"
    if limit is not None:
        url += f"&limit={limit}"
    if offset is not None:
        url += f"&offset={offset}"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.search - idn_search: url: {url}")
        print(f"idnapi.search - idn_search: request body: {data}")

    # invoke the api
    response = requests.post(url, headers=headers, json=data)

    if DEBUG_LOGGING:
        print(f"idnapi.search - idn_search: response headers: {response.headers}")
        print(f"idnapi.search - idn_search: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.search - idn_search: problem performing search query!")
        print("idnapi.search - idn_search: status code: ", response.status_code)
        print("idnapi.search - idn_search: reason: ", response.reason)
        print("idnapi.search - idn_search: text: ", response.text)
        raise Exception("idnapi.search - idn_search: problem performing search query!")
    else:
        print("idnapi.search - idn_search: successfully performed search query")

    # prepare result to return
    result = {
        "response": response.json()
    }
    if response.headers.get("X-Total-Count") is not None:
        result["count"] = int(response.headers["X-Total-Count"])

    if DEBUG_LOGGING:
        print(f"idnapi.search - idn_search: result: {result}")

    print("idnapi.search - idn_search: exit function")
    return result


# search IDN for a specific object by the provided index and id
def idn_search_by_index_and_id(params):
    print("idnapi.search - idn_search_by_index_and_id: enter function")

    config = params["config"]
    headers = params["headers"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/search/{params['index']}/{params['id']}"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.search - idn_search_by_index_and_id: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.search - idn_search_by_index_and_id: response headers: {response.headers}")
        print(f"idnapi.search - idn_search_by_index_and_id: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.search - idn_search_by_index_and_id: problem performing search query!")
        print("idnapi.search - idn_search_by_index_and_id: status code: ", response.status_code)
        print("idnapi.search - idn_search_by_index_and_id: reason: ", response.reason)
        print("idnapi.search - idn_search_by_index_and_id: text: ", response.text)
        raise Exception("idnapi.search - idn_search_by_index_and_id: problem performing search query!")
    else:
        print("idnapi.search - idn_search_by_index_and_id: successfully performed search query")

    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.search - idn_search_by_index_and_id: result: {result}")

    print("idnapi.search - idn_search_by_index_and_id: exit function")
    return result
