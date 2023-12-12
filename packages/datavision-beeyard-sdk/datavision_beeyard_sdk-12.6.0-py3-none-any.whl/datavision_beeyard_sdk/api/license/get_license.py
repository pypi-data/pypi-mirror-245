from ...client import AuthenticatedClient
import json


def read_license_info(*, client: AuthenticatedClient):
    """Read license status.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    dict
        License status.
    """
    url = "{}/api/v1/license".format(client.base_url)
    response = client.get(url, headers=client.token_headers)
    return json.loads(response.content)
