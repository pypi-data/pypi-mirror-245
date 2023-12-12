from ...client import AuthenticatedClient
from ...models.upload_mask_multipart_data import UploadMaskMultipartData


def update(
    id: str,
    overlay_name: str,
    *,
    client: AuthenticatedClient,
    mask_data: UploadMaskMultipartData
):
    """Modify a mask.

    Parameters
    ----------
    id : str
        Id of the target cell.
    overlay_name : str
        Name of target overlay.
    client : AuthenticatedClient
        BeeYard client.
    mask_data : UploadMaskMultipartData
        New mask data.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/overlays/{overlayName}/masks/upload".format(
        client.base_url, id=id, overlayName=overlay_name
    )
    multipart_data = mask_data.to_multipart()
    response = client.patch(url, headers=client.token_headers, files=multipart_data)
    return response
