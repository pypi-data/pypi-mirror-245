from ...client import AuthenticatedClient


def remove(id: str, *, client: AuthenticatedClient, filenames: [str]):
    """Remove files.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    filenames : list[str]
        List of file names.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/files?filenames=".format(client.base_url, id=id)
    for f in filenames:
        url = url + f + "&filenames="
    response = client.delete(url[:-11], headers=client.token_headers)
    return response
