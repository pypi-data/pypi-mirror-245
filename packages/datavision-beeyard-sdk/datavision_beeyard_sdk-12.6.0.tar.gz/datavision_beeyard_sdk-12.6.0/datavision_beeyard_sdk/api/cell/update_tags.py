from ...client import AuthenticatedClient
from ...models.update_tags_dto import UpdateTagsDto
import json


def update(id: str, *, client: AuthenticatedClient, tag_list: UpdateTagsDto):
    """Update tags in cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    tag_list : UpdateTagsDto
        Object containing old tags and new tags.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/updateTags".format(client.base_url, id=id)
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    tags = tag_list.to_dict()
    request_body = json.dumps(tags)
    response = client.post(url, headers=header, data=request_body)
    return response
