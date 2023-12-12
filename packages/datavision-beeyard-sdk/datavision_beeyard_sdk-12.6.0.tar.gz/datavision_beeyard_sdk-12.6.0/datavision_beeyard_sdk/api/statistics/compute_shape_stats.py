from ...client import AuthenticatedClient
import json


def compute(workspace_id: str, *, client: AuthenticatedClient, query: str):
    """Compute statistics on shapes in specific workspace and only on data cells.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.
    query : str
        MongoDB query. It can also be empty "".

    Returns
    -------
    dict
        Dictionary describing the cell.
    """
    url = "{}/api/v1/workspaces/{workspaceId}/shapeTemplates/stats".format(
        client.base_url, workspaceId=workspace_id
    )
    response = client.post(url, headers=client.token_headers, data=query)
    return json.loads(response.content)
