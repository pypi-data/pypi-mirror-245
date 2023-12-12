from ...client import AuthenticatedClient


def delete(workspace_id: str, *, client: AuthenticatedClient):
    """Remove a workspace.

    To be able to remove a workspace, it must be empty.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/workspaces/{workspaceId}".format(
        client.base_url, workspaceId=workspace_id
    )
    response = client.delete(url, headers=client.token_headers)
    return response
