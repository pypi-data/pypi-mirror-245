from ...client import AuthenticatedClient


def read(id: str, *, client: AuthenticatedClient):
    """Read overlays from cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    json string
        Content of the Http response from API as a json.
    """
    url = "{}/api/v1/cells/{id}/overlays".format(client.base_url, id=id)
    response = client.get(url, headers=client.token_headers)
    return response.content
