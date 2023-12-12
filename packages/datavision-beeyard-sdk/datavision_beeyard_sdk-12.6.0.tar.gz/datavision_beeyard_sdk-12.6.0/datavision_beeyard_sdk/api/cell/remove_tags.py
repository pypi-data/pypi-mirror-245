import json
from ...client import AuthenticatedClient
from ...models.tag_dto import TagDto


def delete(id: str, *, client: AuthenticatedClient, tag_list: [TagDto]):
    """Remove tags from cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    tag_list : list[TagDto]
        List of tags to be removed.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/removeTags".format(client.base_url, id=id)
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    tags = [i.to_dict() for i in tag_list]
    request_body = json.dumps(tags)
    response = client.post(url, headers=header, data=request_body)
    return response
