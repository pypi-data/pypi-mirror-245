from ...client import AuthenticatedClient


def add(workspace_id: str, *, client: AuthenticatedClient, json_body: str):
    """Add shape templates to workspace.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.
    json_body : json str
        Json string containing a list of tag templates.

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
    response = client.post(url, headers=header, data=json_body)
    return response
