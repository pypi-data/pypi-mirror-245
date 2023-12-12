from ...client import AuthenticatedClient
from ...models.reference_dto import ReferenceDto
import json


def add(id: str, *, client: AuthenticatedClient, ref_list: [ReferenceDto]):
    """Add references to cell.

    Parameters
    ----------
    id : str
        Target cell id.
    client : AuthenticatedClient
        BeeYard client.
    ref_list : list[ReferenceDto]
        List of references.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/references".format(client.base_url, id=id)
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    refs = [i.to_dict() for i in ref_list]
    request_body = json.dumps(refs)
    response = client.post(url, headers=header, data=request_body)
    return response
