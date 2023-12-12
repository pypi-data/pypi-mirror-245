from ...client import AuthenticatedClient
from ...models.add_files_multipart_data import AddFilesMultipartData


def add(id: str, *, client: AuthenticatedClient, files: AddFilesMultipartData):
    """Add files to cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    files : AddFilesMultipartData
        Object containing list of files to upload.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/files".format(client.base_url, id=id)
    multipart_data = files.to_multipart()
    response = client.post(url, headers=client.token_headers, files=multipart_data)
    return response
