from ...client import AuthenticatedClient


def remove(
    id: str, overlay_name: str, *, client: AuthenticatedClient, shape_ids: [str]
):
    """_summary_

    Parameters
    ----------
    id : str
        Id of the target cell.
    overlay_name : str
        Name of the target overlay.
    client : AuthenticatedClient
        BeeYard client.
    shape_ids : list[str]
        List of shape ids to be removed.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/overlays/{overlayName}?shapeIds=".format(
        client.base_url, id=id, overlayName=overlay_name
    )
    for i in shape_ids:
        url = url + i + "&shapeIds="
    response = client.delete(url[:-10], headers=client.token_headers)
    return response
