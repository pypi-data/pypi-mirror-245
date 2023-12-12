import json
from ...client import AuthenticatedClient
from ...types import strict_types


@strict_types
def modify(id: str, document_name: str, *, client: AuthenticatedClient, json_body: str):
    """Modify a document in cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    document_name : str
    client : AuthenticatedClient
        BeeYard client.
    json_body : json str
        New content.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/documents/{documentName}".format(
        client.base_url, id=id, documentName=document_name
    )
    request = {}
    request["content"] = json.loads(json_body)
    request_body = json.dumps(request)
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    response = client.patch(url, headers=header, data=request_body)
    return response
