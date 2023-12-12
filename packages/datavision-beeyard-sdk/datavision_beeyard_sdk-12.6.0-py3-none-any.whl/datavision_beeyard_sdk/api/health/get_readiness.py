from ...client import AuthenticatedClient


def ready(*, client: AuthenticatedClient):
    """Get readiness.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    str
        Liveness status.
    """
    url = "{}/api/v1/health/ready".format(client.base_url)
    response = client.get(url, headers=client.token_headers)
    return response.content
