from ...client import AuthenticatedClient


def read(id: str, overlay_name: str, shape_id: str, *, client: AuthenticatedClient):
    """Read a shape from an overlay.

    Parameters
    ----------
    id : str
        Id of the target cell.
    overlay_name : str
        Name of the target overlay.
    shape_id : str
        Id of the shape to read.
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    json string
        Content of the Http response from API as a json.
    """
    url = "{}/api/v1/cells/{id}/overlays/{overlayName}/shapes/{shapeId}".format(
        client.base_url, id=id, overlayName=overlay_name, shapeId=shape_id
    )
    response = client.get(url, headers=client.token_headers)
    return response.content
