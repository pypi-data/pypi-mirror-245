BeeYard-SDK: A client library for accessing Hive API
####################################################

Release notes
=============

Release notes are available on the documentation web page https://docs.beeyard.ai/docs/reference/sdk/python/release-notes/.

Installation
============
To use the package, just install it via pip (or preferred package manager):

.. code-block:: bash

    pip install datavision-beeyard-sdk

or use Poetry package manager to create your virtual environment and just add the SDK with:

.. code-block:: bash

    poetry add datavision-beeyard-sdk

Now all functionalities are ready to be imported inside your Python project!

Initialize a BeeYard client
===========================
Authentication is with authenticated client:

.. code-block:: python

    from beeyard_sdk import AuthenticatedClient
    client = AuthenticatedClient('https://demo.beeyard.ai/hive/', username, password)

It is possible to specify the *max_waiting_time_ms* parameter (in milliseconds) when creating the client object in order to avoid connectivity problems.
It specifies the max time within which the client tries to repeatedly send the request, in case of connectivity errors. After that time,
a ConnectionError will be raised. Default value is 0.

.. code-block:: python

    client = AuthenticatedClient('https://demo.beeyard.ai/hive/', username, password, max_waiting_time_ms=1000)

As login endpoint will be updated, some optional parameters are provided, that can be set to point to the new endpoint:

.. code-block:: python

    client = AuthenticatedClient('https://demo.beeyard.ai/hive/', username, password, max_waiting_time_ms=1000, client_id="byard", client_secret="", login_url=None)

where *login_url* is the new endpoint uri.

It is possible to log in using client credentials as follows:

.. code-block:: python

    client = AuthenticatedClient('https://demo.beeyard.ai/hive/', grant_type="client_credentials", client_id="the_client_id", client_secret="the_client_secret", login_url="https://demo.beeyard.ai/id/")

Another option is to use a valid access token to initialize the client:

.. code-block:: python

    client = AuthenticatedClient('https://demo.beeyard.ai/hive/', use_token=True, token="valid_token")

Example usage
=============

.. code-block:: python

    from datavision_beeyard_sdk.models import WorkspaceDescriptorDto
    from datavision_beeyard_sdk.api.workspace import create_workspace

    workspace_desc = WorkspaceDescriptorDto(name="test", namespace="test")
    create_workspace.create(client=client, request_body=workspace_desc)

Documentation
=============

Complete documentation can be found at https://docs.beeyard.ai/docs/reference/sdk/python/methods_reference/.
