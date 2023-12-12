from ...client import AuthenticatedClient


def read(workspace_id: str, *, client: AuthenticatedClient):
    """Read a workspace information.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    json string
        Content of the Http response from API as a json.
    """
    url = "{}/api/v1/workspaces/{workspaceId}".format(
        client.base_url, workspaceId=workspace_id
    )
    response = client.get(url, headers=client.token_headers)
    return response.content
