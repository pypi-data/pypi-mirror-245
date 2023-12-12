# -*- coding: utf-8 -*-
from ...client import AuthenticatedClient
from ...models.property_dto import PropertyDto
import json


def update(id: str, *, client: AuthenticatedClient, prop_update: PropertyDto):
    """Modify cell property

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    prop_update : PropertyDto
        Cell property.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/properties".format(client.base_url, id=id)
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    prop = prop_update.to_dict()
    request_body = json.dumps(prop)
    response = client.patch(url, headers=header, data=request_body)
    return response
