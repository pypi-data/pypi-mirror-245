from ...client import AuthenticatedClient


def update(
    id: str,
    client: AuthenticatedClient,
    *,
    overlay_name: str,
    layer_name: str,
    json_body: str
):
    """Rename a layer.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    overlay_name : str
        Name of the target overlay.
    layer_name : str
        Old layer name.
    json_body : json str
        Json string with new layer name.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/overlays/{overlayName}/layers/{layerName}".format(
        client.base_url, id=id, overlayName=overlay_name, layerName=layer_name
    )
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    response = client.patch(url, headers=header, data=json_body)
    return response
