from ...client import AuthenticatedClient
from ...models.add_documents_multipart_data import AddDocumentsMultipartData


def add(
    id: str, *, client: AuthenticatedClient, multipart_data: AddDocumentsMultipartData
):
    """Add documents to cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    multipart_data : AddDocumentsMultipartData
        Object containing list of documents to be uploaded.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/documents".format(client.base_url, id=id)
    request_body = multipart_data.to_multipart()
    response = client.post(url, headers=client.token_headers, files=request_body)
    return response
