from ...client import AuthenticatedClient


def remove(id: str, *, client: AuthenticatedClient, namespace=None):
    """Remove cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    namespace : str, optional
        Namespace of the cell to remove, by default None

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}".format(client.base_url, id=id)
    response = client.delete(url, headers=client.token_headers)
    return response
