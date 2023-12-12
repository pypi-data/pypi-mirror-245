from ...client import AuthenticatedClient


def add(workspace_id: str, *, client: AuthenticatedClient, json_body: str):
    """Replace shape template in workspace.

    If shape template does not exist, it is saved.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.
    json_body : json str
        Json string containing shape template.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/workspaces/{workspaceId}/shapeTemplates".format(
        client.base_url, workspaceId=workspace_id
    )
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    response = client.put(url, headers=header, data=json_body)
    return response
