# idnapi

idnapi is a Python library that implements an API client for SailPoint IdentityNow's REST API.

## Authors
- [Mark Spain](mailto:Mark.Spain@ey.com?subject=idnapi%20-%20%28IdentityNow%20Python%20SDK%29)

## Installation
### Pip
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install idnapi.
```bash
pip install idnapi
```
NOTE: This has not yet been published to PyPI, so the above will not work for the time being. Please install manually.

### Manual
#### Prerequisites
1. Install python build packages:
    ```bash
    pip install build
    ```
2. If using virtual environments (recommended), install pipenv:
    ```bash
   pip install pipenv
    ```

#### Instructions
1. Clone this repository.
2. From within the repository root directory, run the following command to build the module:
    ```bash
    python -m build
    ```
3. Copy the resulting wheel file (ex: `dist/idnapi-0.0.1-py3-none-any.whl`) to your project directory. Note that the name will match the version that you built.
4. Change directory into your project directory:
    ```bash
    cd /path/to/your/project
    ```
5. From within your project directory, run one of the following commands to install your wheel file (make sure the file name matches what was produced when you built the module):
   ##### Using pipenv
    ```bash
    pipenv install idnapi-0.0.1-py3-none-any.whl
    ```
   ##### Using pip 
   ```bash
    pip install idnapi-0.0.1-py3-none-any.whl
    ```
6. Activate this projects virtualenv (if using pipenv):
    ```bash
    pipenv shell
    ```

## Usage
### Authentication
The IDNClient class requires the following parameters to be passed in:
- `tenant_name`: The name of your IdentityNow tenant.
- `client_id`: The client ID of your IdentityNow API client.
- `client_secret`: The client secret of your IdentityNow API client.

In general, the `client_id` and `client_secret` should be a PAT (Personal Access Token) that was created in IdentityNow, assigned the necessary scopes (such as `sp:scopes:all`), under an identity that has the `ORG_ADMIN` user level in IdentityNow.

### Example
```python
from idnapi import IDNClient

# setup IdentityNow tenant configuration
TENANT_NAME = "<tenant name>"
CLIENT_ID = "<client id>"
CLIENT_SECRET = "<client secret>"

# create an IDNClient object
idn_client = IDNClient(TENANT_NAME, CLIENT_ID, CLIENT_SECRET)

# prepare parameters to pass into the Search API
params = {
    "offset": 0,
    "limit": 1,
    "count": True,
    "data": {
        "indices": ["identities"],
        "query": {
            "query": "*"
        },
        "sort": ["id"]
    }
}

# invoke the Search API endpoint with the prepared parameters
search_result = idn_client.search(params)

# get the total number of records from the search result
# note that params must contain: "count": True
total = search_result["count"]
print(f"total: {total}")

# get the response JSON from the search result
# returns a JSON array of JSON objects
objects = search_result["response"]
print(f"objects: {objects}")
print(f"first result: {objects[0]}")
print(f"first result id: {objects[0]['id']}")
print(f"first result displayName: {objects[0]['displayName']}")
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)