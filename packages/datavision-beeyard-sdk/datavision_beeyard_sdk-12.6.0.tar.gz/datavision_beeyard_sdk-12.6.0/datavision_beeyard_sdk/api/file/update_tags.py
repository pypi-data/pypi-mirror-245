from ...client import AuthenticatedClient
from ...models.update_tags_dto import UpdateTagsDto
import json


def update(
    id: str, filename: str, *, client: AuthenticatedClient, tag_list: UpdateTagsDto
):
    """Update file tags.

    Parameters
    ----------
    id : str
        Target cell id.
    filename : str
    client : AuthenticatedClient
        BeeYard client.
    tag_list : UpdateTagsDto
        Object containing list of old tags and new ones.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/files/{filename}/updateTags".format(
        client.base_url, id=id, filename=filename
    )
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    tags = tag_list.to_dict()
    request_body = json.dumps(tags)
    response = client.post(url, headers=header, data=request_body)
    return response
