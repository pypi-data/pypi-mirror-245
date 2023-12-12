from ...client import AuthenticatedClient
import json


def compute(workspace_id: str, *, client: AuthenticatedClient, query: str):
    """Compute statistics on tags in specific workspace and only on data cells.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.
    query : str, optional
        MongoDB query, by default ""

    Returns
    -------
    dict
        Dictionary describing the cell.
    """
    url = "{}/api/v1/workspaces/{workspaceId}/tags/stats".format(
        client.base_url, workspaceId=workspace_id
    )
    response = client.post(url, headers=client.token_headers, data=query)
    return json.loads(response.content)
