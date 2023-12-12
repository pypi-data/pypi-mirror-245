from ...client import AuthenticatedClient
from ...models.favorite_query_dto import FavoriteQueryDto
import json


def update(
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    query_name: str,
    query_update: FavoriteQueryDto
):
    """Modify a favorite query.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.
    query_name : str
        Name of target query.
    query_update : FavoriteQueryDto
        Object containing the new query.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/workspaces/{workspaceId}/favoriteQueries/{query_name}".format(
        client.base_url, workspaceId=workspace_id, query_name=query_name
    )
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    json_qta = json.dumps(query_update.to_dict())
    response = client.patch(url, headers=header, data=json_qta)
    return response
