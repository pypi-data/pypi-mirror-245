from ...client import AuthenticatedClient


def read(id: str, filename: str, *, client: AuthenticatedClient):
    """Read file from cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    filename : str
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    json string
        Content of the Http response from API as a json.
    """
    url = "{}/api/v1/cells/{id}/files/{filename}".format(
        client.base_url, id=id, filename=filename
    )
    response = client.get(url, headers=client.token_headers)
    return response.content
