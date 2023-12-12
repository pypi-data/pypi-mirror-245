from ...client import AuthenticatedClient


def read(id: str, *, client: AuthenticatedClient, image_name: str):
    """Read image thumbnail.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    image_name : str

    Returns
    -------
    bytes
        Bytes stream of the thumbnail.
    """
    url = "{}/api/v1/cells/{id}/images/{imageName}/thumbnail".format(
        client.base_url, id=id, imageName=image_name
    )
    response = client.get(url, headers=client.token_headers)
    return response.content
