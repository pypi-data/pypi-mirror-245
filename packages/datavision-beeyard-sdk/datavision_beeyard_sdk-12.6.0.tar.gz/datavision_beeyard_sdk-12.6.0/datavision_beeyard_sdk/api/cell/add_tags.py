import json
from ...client import AuthenticatedClient
from ...models.tag_dto import TagDto


def add(id: str, *, client: AuthenticatedClient, tag_list: [TagDto]):
    """Add tags to cell.

    Parameters
    ----------
    id : str
        Target cell id.
    client : AuthenticatedClient
        BeeYard client.
    tag_list : list[TagDto]
        List of tags.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/addTags".format(client.base_url, id=id)
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    tags = [i.to_dict() for i in tag_list]
    request_body = json.dumps(tags)
    response = client.post(url, headers=header, data=request_body)
    return response
