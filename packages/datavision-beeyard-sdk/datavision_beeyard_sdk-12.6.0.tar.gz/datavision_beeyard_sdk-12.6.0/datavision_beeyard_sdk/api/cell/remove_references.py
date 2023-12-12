from ...client import AuthenticatedClient


def delete(id: str, *, client: AuthenticatedClient, keys: [str]):
    """Remove references from cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    keys : list[str]
        List of keys of the references to be removed.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/references?keys=".format(client.base_url, id=id)
    for k in keys:
        url = url + k + "&keys="
    response = client.delete(url[:-6], headers=client.token_headers)
    return response
