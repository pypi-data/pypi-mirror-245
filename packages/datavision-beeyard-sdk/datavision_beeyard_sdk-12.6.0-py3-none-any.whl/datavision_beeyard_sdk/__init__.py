"""A client library for accessing Hive API.

This SDK is used to interact with the BeeYard platform.

Classes and Modules
-------------------
- AuthenticatedClient
    Is the class used to authenticate the user on the BeeYard platform.

- helpers
    Module containing helper methods.

- api
    Module that contains methods for accessing the BeeYard APIs.

- models
    Module that contains all the data models used in inputs/outputs.

- types
    Module that defines useful custom types to interact with BeeYard, like File or Response.

- exceptions
    Class for error handling in shape manipulation.

Examples
--------
>>> from datavision_beeyard_sdk import AuthenticatedClient
>>> from datavision_beeyard_sdk.api.license import get_license
>>> client = AuthenticatedClient("http://localhost:8018/hive/", "tester", "foobar")
>>> get_license.read_license_info(client=client)
    {'isValid': True, 'licenseType': 'Subscription', 'created': '2023-02-02T14:13:00.401Z',
     'expiry': '2024-02-01T00:00:00Z', 'maxUsers': 5, 'maxMachines': 5}

"""
from .client import AuthenticatedClient
