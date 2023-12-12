from ...client import AuthenticatedClient


def delete(id: str, filename: str, *, client: AuthenticatedClient, keys: [str]):
    """Remove properties from file.

    Parameters
    ----------
    id : str
        Target cell id.
    filename : str
    client : AuthenticatedClient
        BeeYard client.
    keys : list[str]
        List of property keys to be removed.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/files/{filename}/properties?keys=".format(
        client.base_url, id=id, filename=filename
    )
    for k in keys:
        url = url + k + "&keys="
    response = client.delete(url[:-6], headers=client.token_headers)
    return response
