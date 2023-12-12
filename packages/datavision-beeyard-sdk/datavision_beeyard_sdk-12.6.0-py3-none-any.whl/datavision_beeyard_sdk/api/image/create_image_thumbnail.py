from ...client import AuthenticatedClient


def create(id: str, *, client: AuthenticatedClient, image_name: str):
    """Create image thumbnail.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    image_name : str

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/images/{imageName}/thumbnail".format(
        client.base_url, id=id, imageName=image_name
    )
    response = client.post(url, headers=client.token_headers)
    return response.content
