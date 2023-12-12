"""
idnapi.accounts.py
~~~~~~~~~~~~~~~~~~
Author: Mark Spain <Mark.Spain@ey.com>

Description:
This module implements the Accounts endpoints of the IdentityNow REST API.
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

# search IDN for accounts using the provided criteria (filters)
def idn_list_accounts(params):
    print("idnapi.accounts - idn_list_accounts: enter function")

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
    url = f"https://{config['api_host']}/v3/accounts?count={count}"
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
        print(f"idnapi.accounts - idn_list_accounts: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_list_accounts: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_list_accounts: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_list_accounts: problem searching for accounts!")
        print("idnapi.accounts - idn_list_accounts: status code: ", response.status_code)
        print("idnapi.accounts - idn_list_accounts: reason: ", response.reason)
        print("idnapi.accounts - idn_list_accounts: text: ", response.text)
        raise Exception("idnapi.accounts - idn_list_accounts: problem searching for accounts!")
    else:
        print("idnapi.accounts - idn_list_accounts: successfully retrieved accounts")

    # prepare result to return
    result = {
        "response": response.json()
    }
    if response.headers.get("X-Total-Count") is not None:
        result["count"] = int(response.headers["X-Total-Count"])

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_list_accounts: result: {result}")

    print("idnapi.accounts - idn_list_accounts: exit function")
    return result


# get an account by id
def idn_get_account_by_id(params):
    print("idnapi.accounts - idn_get_account_by_id: enter function")

    config = params["config"]
    headers = params["headers"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/accounts/{params['id']}"

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_get_account_by_id: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_get_account_by_id: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_get_account_by_id: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_get_account_by_id: problem retrieving account!")
        print("idnapi.accounts - idn_get_account_by_id: status code: ", response.status_code)
        print("idnapi.accounts - idn_get_account_by_id: reason: ", response.reason)
        print("idnapi.accounts - idn_get_account_by_id: text: ", response.text)
        raise Exception("idnapi.accounts - idn_get_account_by_id: problem retrieving account!")
    else:
        print("idnapi.accounts - idn_get_account_by_id: successfully retrieved account")

    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_get_account_by_id: result: {result}")

    print("idnapi.accounts - idn_get_account_by_id: exit function")
    return result


# create an account
def idn_create_account(params):
    print("idnapi.accounts - idn_create_account: enter function")

    config = params["config"]
    headers = params["headers"]
    data = params["data"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/accounts"

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_create_account: url: {url}")
        print(f"idnapi.accounts - idn_create_account: request body: {data}")

    # invoke the api
    response = requests.post(url, headers=headers, json=data)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_create_account: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_create_account: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_create_account: problem creating account!")
        print("idnapi.accounts - idn_create_account: status code: ", response.status_code)
        print("idnapi.accounts - idn_create_account: reason: ", response.reason)
        print("idnapi.accounts - idn_create_account: text: ", response.text)
        raise Exception("idnapi.accounts - idn_create_account: problem creating account!")
    else:
        print("idnapi.accounts - idn_create_account: successfully created account")

    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_create_account: result: {result}")

    print("idnapi.accounts - idn_create_account: exit function")
    return result


# update an account (partial)
def idn_update_account_partial(params):
    print("idnapi.accounts - idn_update_account_partial: enter function")

    config = params["config"]
    headers = params["headers"]
    data = params["data"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/accounts/{params['id']}"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_update_account_partial: url: {url}")
        print(f"idnapi.accounts - idn_update_account_partial: request body: {data}")

    # invoke the api
    response = requests.patch(url, headers=headers, json=data)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_update_account_partial: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_update_account_partial: response body: {response.json()}")
    
    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_update_account_partial: problem updating account!")
        print("idnapi.accounts - idn_update_account_partial: status code: ", response.status_code)
        print("idnapi.accounts - idn_update_account_partial: reason: ", response.reason)
        print("idnapi.accounts - idn_update_account_partial: text: ", response.text)
        raise Exception("idnapi.accounts - idn_update_account_partial: problem updating account!")
    else:
        print("idnapi.accounts - idn_update_account_partial: successfully updated account")
    
    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_update_account_partial: result: {result}")

    print("idnapi.accounts - idn_update_account_partial: exit function")
    return result


# update an account (full)
def idn_update_account_full(params):
    print("idnapi.accounts - idn_update_account_full: enter function")

    config = params["config"]
    headers = params["headers"]
    data = params["data"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/accounts/{params['id']}"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_update_account_full: url: {url}")
        print(f"idnapi.accounts - idn_update_account_full: request body: {data}")

    # invoke the api
    response = requests.put(url, headers=headers, json=data)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_update_account_full: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_update_account_full: response body: {response.json()}")
    
    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_update_account_full: problem updating account!")
        print("idnapi.accounts - idn_update_account_full: status code: ", response.status_code)
        print("idnapi.accounts - idn_update_account_full: reason: ", response.reason)
        print("idnapi.accounts - idn_update_account_full: text: ", response.text)
        raise Exception("idnapi.accounts - idn_update_account_full: problem updating account!")
    else:
        print("idnapi.accounts - idn_update_account_full: successfully updated account")
    
    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_update_account_full: result: {result}")

    print("idnapi.accounts - idn_update_account_full: exit function")
    return result


# delete an account
def idn_delete_account(params):
    print("idnapi.accounts - idn_delete_account: enter function")

    config = params["config"]
    headers = params["headers"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/accounts/{params['id']}"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_delete_account: url: {url}")

    # invoke the api
    response = requests.delete(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_delete_account: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_delete_account: response body: {response.json()}")
    
    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_delete_account: problem deleting account!")
        print("idnapi.accounts - idn_delete_account: status code: ", response.status_code)
        print("idnapi.accounts - idn_delete_account: reason: ", response.reason)
        print("idnapi.accounts - idn_delete_account: text: ", response.text)
        raise Exception("idnapi.accounts - idn_delete_account: problem deleting account!")
    else:
        print("idnapi.accounts - idn_delete_account: successfully deleted account")
    
    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_delete_account: result: {result}")

    print("idnapi.accounts - idn_delete_account: exit function")
    return result


# get an account's entitlements by account id
def idn_get_account_entitlements_by_id(params):
    print("idnapi.accounts - idn_get_account_entitlements_by_id: enter function")

    config = params["config"]
    headers = params["headers"]
    
    count = params["count"] if params.get("count") is not None else False
    limit = params.get("limit")
    offset = params.get("offset")

    # convert count (bool) to lowercase string
    count = str(count).lower()

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/accounts/{params['id']}/entitlements?count={count}"
    if limit is not None:
        url += f"&limit={limit}"
    if offset is not None:
        url += f"&offset={offset}"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_get_account_entitlements_by_id: url: {url}")

    # invoke the api
    response = requests.get(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_get_account_entitlements_by_id: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_get_account_entitlements_by_id: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_get_account_entitlements_by_id: problem retrieving account entitlements!")
        print("idnapi.accounts - idn_get_account_entitlements_by_id: status code: ", response.status_code)
        print("idnapi.accounts - idn_get_account_entitlements_by_id: reason: ", response.reason)
        print("idnapi.accounts - idn_get_account_entitlements_by_id: text: ", response.text)
        raise Exception("idnapi.accounts - idn_get_account_entitlements_by_id: problem retrieving account entitlements!")
    else:
        print("idnapi.accounts - idn_get_account_entitlements_by_id: successfully retrieved account entitlements")

    # prepare result to return
    result = {
        "response": response.json()
    }
    if response.headers.get("X-Total-Count") is not None:
        result["count"] = int(response.headers["X-Total-Count"])
    
    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_get_account_entitlements_by_id: result: {result}")

    print("idnapi.accounts - idn_get_account_entitlements_by_id: exit function")
    return result


# reload an account
def idn_reload_account(params):
    print("idnapi.accounts - idn_reload_account: enter function")

    config = params["config"]
    headers = params["headers"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/accounts/{params['id']}/reload"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_reload_account: url: {url}")

    # invoke the api
    response = requests.post(url, headers=headers)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_reload_account: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_reload_account: response body: {response.json()}")

    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_reload_account: problem reloading account!")
        print("idnapi.accounts - idn_reload_account: status code: ", response.status_code)
        print("idnapi.accounts - idn_reload_account: reason: ", response.reason)
        print("idnapi.accounts - idn_reload_account: text: ", response.text)
        raise Exception("idnapi.accounts - idn_reload_account: problem reloading account!")
    else:
        print("idnapi.accounts - idn_reload_account: successfully reloaded account")

    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_reload_account: result: {result}")

    print("idnapi.accounts - idn_reload_account: exit function")
    return result


# enable an account
def idn_enable_account(params):
    print("idnapi.accounts - idn_enable_account: enter function")

    config = params["config"]
    headers = params["headers"]
    data = params["data"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/accounts/{params['id']}/enable"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_enable_account: url: {url}")
        print(f"idnapi.accounts - idn_enable_account: request body: {data}")
    
    # invoke the api
    response = requests.post(url, headers=headers, json=data)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_enable_account: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_enable_account: response body: {response.json()}")
    
    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_enable_account: problem enabling account!")
        print("idnapi.accounts - idn_enable_account: status code: ", response.status_code)
        print("idnapi.accounts - idn_enable_account: reason: ", response.reason)
        print("idnapi.accounts - idn_enable_account: text: ", response.text)
        raise Exception("idnapi.accounts - idn_enable_account: problem enabling account!")
    else:
        print("idnapi.accounts - idn_enable_account: successfully enabled account")
    
    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_enable_account: result: {result}")
    
    print("idnapi.accounts - idn_enable_account: exit function")
    return result


# disable an account
def idn_disable_account(params):
    print("idnapi.accounts - idn_disable_account: enter function")

    config = params["config"]
    headers = params["headers"]
    data = params["data"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/accounts/{params['id']}/disable"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_disable_account: url: {url}")
        print(f"idnapi.accounts - idn_disable_account: request body: {data}")
    
    # invoke the api
    response = requests.post(url, headers=headers, json=data)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_disable_account: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_disable_account: response body: {response.json()}")
    
    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_disable_account: problem disabling account!")
        print("idnapi.accounts - idn_disable_account: status code: ", response.status_code)
        print("idnapi.accounts - idn_disable_account: reason: ", response.reason)
        print("idnapi.accounts - idn_disable_account: text: ", response.text)
        raise Exception("idnapi.accounts - idn_disable_account: problem disabling account!")
    else:
        print("idnapi.accounts - idn_disable_account: successfully disabled account")
    
    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_disable_account: result: {result}")
    
    print("idnapi.accounts - idn_disable_account: exit function")
    return result


# unlock an account
def idn_unlock_account(params):
    print("idnapi.accounts - idn_unlock_account: enter function")

    config = params["config"]
    headers = params["headers"]
    data = params["data"]

    # prepare the url with query parameters
    url = f"https://{config['api_host']}/v3/accounts/{params['id']}/unlock"

    # encode the url
    url = requote_uri(url)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_unlock_account: url: {url}")
        print(f"idnapi.accounts - idn_unlock_account: request body: {data}")
    
    # invoke the api
    response = requests.post(url, headers=headers, json=data)

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_unlock_account: response headers: {response.headers}")
        print(f"idnapi.accounts - idn_unlock_account: response body: {response.json()}")
    
    # check for errors
    if response.status_code < 200 or response.status_code > 299:
        print("idnapi.accounts - idn_unlock_account: problem unlocking account!")
        print("idnapi.accounts - idn_unlock_account: status code: ", response.status_code)
        print("idnapi.accounts - idn_unlock_account: reason: ", response.reason)
        print("idnapi.accounts - idn_unlock_account: text: ", response.text)
        raise Exception("idnapi.accounts - idn_unlock_account: problem unlocking account!")
    else:
        print("idnapi.accounts - idn_unlock_account: successfully unlocked account")
    
    # prepare result to return
    result = {
        "response": response.json()
    }

    if DEBUG_LOGGING:
        print(f"idnapi.accounts - idn_unlock_account: result: {result}")
    
    print("idnapi.accounts - idn_unlock_account: exit function")
    return result
