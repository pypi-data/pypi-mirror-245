from ...client import AuthenticatedClient
import json


def add(
    id: str,
    overlay_name: str,
    layer_name: str,
    *,
    client: AuthenticatedClient,
    shape_list: []
):
    """Add shapes to overlay.

    Parameters
    ----------
    id : str
        Id of the target cell.
    overlay_name : str
        Name of the target overlay.
    layer_name : str
        Name of the target layer. If does not exist, it is created.
    client : AuthenticatedClient
        BeeYard client.
    shape_list : list[dict]
        List of dictionary. Each dictionary is a shape.

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
    json_body = json.dumps(shape_list)
    response = client.post(url, headers=header, data=json_body)
    return response
