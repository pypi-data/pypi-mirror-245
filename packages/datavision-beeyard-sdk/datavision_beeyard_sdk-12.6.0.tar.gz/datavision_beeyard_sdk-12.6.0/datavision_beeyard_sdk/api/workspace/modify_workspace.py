from ...client import AuthenticatedClient


def update(workspace_id: str, *, client: AuthenticatedClient, json_body: str):
    """Modify workspace name.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.
    json_body : json str
        Json string containing the new workspace name.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/workspaces/{workspaceId}".format(
        client.base_url, workspaceId=workspace_id
    )
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    response = client.patch(url, headers=header, data=json_body)
    return response
