from ...client import AuthenticatedClient


def live(*, client: AuthenticatedClient):
    """Get liveness.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    str
        Liveness status.
    """
    url = "{}/api/v1/health/live".format(client.base_url)
    response = client.get(url, headers=client.token_headers)
    return response.headers
