"""
idnclient.py
~~~~~~~~~~~~
Author: Mark Spain <Mark.Spain@ey.com>

Description:
This module implements an API client for IdentityNow's REST API.
"""
import time
from datetime import datetime
from .oauth import idn_get_oauth_token
from .accessprofiles import idn_list_access_profiles, idn_get_access_profile_by_id
from .entitlements import idn_list_entitlements, idn_get_entitlement_by_id
from .roles import idn_list_roles, idn_get_role_by_id
from .search import idn_search, idn_search_by_index_and_id
from .workgroups import idn_get_governance_group_by_id, idn_list_governance_groups, idn_list_governance_group_members


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG_LOGGING = False


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------

# function to sleep for a given number of milliseconds
def sleep(milliseconds):
    time.sleep(milliseconds / 1000)


# function to get the current time in milliseconds
def current_time_millis():
    return datetime.now().timestamp() * 1000


# ------------------------------------------------------------------------------
# IdentityNow API Client
# ------------------------------------------------------------------------------

class IDNClient:

    # configuration passed into the constructor
    config = {}

    # default_expiration is the number of milliseconds before the API token expires
    default_expiration = 3300000  # 55 minutes in milliseconds (token expires after 1 hour)

    # token and expiration are used to cache the API access token
    token = ""
    expiration = 0

    # sleep_duration is the number of milliseconds to sleep between API calls
    sleep_duration = 100  # 100 milliseconds

    # last_call_time is used to throttle calls to the IDN API
    last_call_time = 0

    # constructor
    def __init__(self, tenant_name, client_id, client_secret):
        print("IDNClient - __init__: enter function")
        self.config = {
            "tenant_name": tenant_name,
            "client_id": client_id,
            "client_secret": client_secret,
            "tenant_host": f"{tenant_name}.identitynow.com",
            "api_host": f"{tenant_name}.api.identitynow.com"
        }
        print("IDNClient - __init__: exit function")

    # function to sleep until it is safe to make another API call, used to throttle calls to the IDN API
    def self_throttle(self, min_time_between_calls, include_buffer):
        print("IDNClient - self_throttle: enter function")
        if include_buffer:
            # include 20% buffer
            min_time_between_calls *= 1.2
        while (current_time_millis() - self.last_call_time) < min_time_between_calls:
            print("IDNClient - self_throttle: waiting...")
            sleep(self.sleep_duration)
        print("IDNClient - self_throttle: exit function")

    # function to get an API access token and cache it, or fetch a new on if it has expired
    def get_access_token(self):
        print("IDNClient - get_access_token: enter function")
        if self.expiration > current_time_millis():
            print("IDNClient - get_access_token: token is not expired, returning cached token")
            print("IDNClient - get_access_token: exit function")
            return self.token
        elif self.token == "":
            print("IDNClient - get_access_token: token is empty, fetching new token...")
        else:
            print("IDNClient - get_access_token: token is expired, fetching new token...")

        params = {
            "config": self.config,
            "headers": {
                "content-type": "application/json",
                "accept": "application/json"
            }
        }

        self.token = idn_get_oauth_token(params)
        self.expiration = current_time_millis() + self.default_expiration

        print(f"IDNClient - get_access_token: returning access token, expires in {self.expiration}")
        print("IDNClient - get_access_token: exit function")
        return self.token

    # function to get the headers needed to make an API call, including the access token
    def get_headers(self):
        print("IDNClient - get_headers: enter function")
        token = self.get_access_token()
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "authorization": f"Bearer {token}"
        }
        print("IDNClient - get_headers: exit function")
        return headers

    # function to prepare the parameters for an API call, including the headers
    def prepare_params(self, params):
        print("IDNClient - prepare_params: enter function")
        params["config"] = self.config
        params["headers"] = params["headers"] if "headers" in params else self.get_headers()  # use the provided headers if they exist
        print("IDNClient - prepare_params: exit function")
        return params

    # function to invoke an API call, throttling the calls to the IDN API
    def invoke_throttled(self, min_time_between_calls, func, params):
        print("IDNClient - invoke_throttled: enter function")
        if DEBUG_LOGGING:
            print(f"IDNClient - invoke_throttled: calling function: {func.__name__} with params: {params}")
        self.self_throttle(min_time_between_calls, True)
        result = func(self.prepare_params(dict(params)))  # clone the params dict to avoid modifying the original
        self.last_call_time = current_time_millis()
        if DEBUG_LOGGING:
            print(f"IDNClient - invoke_throttled: function: {func.__name__} returned: {result}")
        print("IDNClient - invoke_throttled: exit function")
        return result

    # throttled call to idn_list_access_profiles
    def list_access_profiles(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_list_access_profiles, params)

    # throttled call to idn_get_access_profile_by_id
    def get_access_profile_by_id(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_get_access_profile_by_id, params)

    # throttled call to idn_list_entitlements
    def list_entitlements(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_list_entitlements, params)

    # throttled call to idn_get_entitlement_by_id
    def get_entitlement_by_id(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_get_entitlement_by_id, params)

    # throttled call to idn_list_roles
    def list_roles(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_list_roles, params)

    # throttled call to idn_get_role_by_id
    def get_role_by_id(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_get_role_by_id, params)

    # throttled call to idn_list_governance_groups
    def list_governance_groups(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_list_governance_groups, params)

    # throttled call to idn_get_governance_group_by_id
    def get_governance_group_by_id(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_get_governance_group_by_id, params)

    # throttled call to idn_list_governance_group_members
    def list_governance_group_members(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_list_governance_group_members, params)

    # throttled call to idn_search
    def search(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_search, params)

    # throttled call to idn_search_by_index_and_id
    def search_by_index_and_id(self, params):
        min_time_between_calls = 100  # 0.1 seconds in milliseconds
        return self.invoke_throttled(min_time_between_calls, idn_search_by_index_and_id, params)
