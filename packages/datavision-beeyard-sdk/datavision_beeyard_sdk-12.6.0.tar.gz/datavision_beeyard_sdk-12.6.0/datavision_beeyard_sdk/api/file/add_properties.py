import json
from ...client import AuthenticatedClient
from ...models.property_dto import PropertyDto


def add(
    id: str, filename: str, *, client: AuthenticatedClient, props_list: [PropertyDto]
):
    """Add properties to file.

    Parameters
    ----------
    id : str
        Target cell id.
    filename : str
    client : AuthenticatedClient
        BeeYard client.
    props_list : list[PropertyDto]
        List of properties.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/files/{filename}/properties".format(
        client.base_url, id=id, filename=filename
    )
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    props = [i.to_dict() for i in props_list]
    request_body = json.dumps(props)
    response = client.post(url, headers=header, data=request_body)
    return response
