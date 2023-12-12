from ...client import AuthenticatedClient
from ...models.add_images_multipart_data import AddImagesMultipartData


def add(
    id: str, *, client: AuthenticatedClient, multipart_data: AddImagesMultipartData
):
    """Add images in cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    multipart_data : AddImagesMultipartData
        Object containing list of images to be added.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/images".format(client.base_url, id=id)
    request_body = multipart_data.to_multipart()
    response = client.post(url, headers=client.token_headers, files=request_body)
    return response
