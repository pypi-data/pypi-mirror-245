from ...client import AuthenticatedClient


def version(*, client: AuthenticatedClient):
    """Get BeeYard version

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    json string
        Content of the Http response from API as a json.
    """
    url = "{}/api/v1/version".format(client.base_url)
    response = client.get(url, headers=client.token_headers)
    return response.content
