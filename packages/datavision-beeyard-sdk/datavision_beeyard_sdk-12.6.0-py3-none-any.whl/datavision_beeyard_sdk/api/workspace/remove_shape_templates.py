from ...client import AuthenticatedClient


def delete(workspace_id: str, *, client: AuthenticatedClient, template_list: [str]):
    """Remove shape templates from workspace.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.
    template_list : list[str]
        List of shape templates to be removed.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/workspaces/{workspaceId}/shapeTemplates?shapes=".format(
        client.base_url, workspaceId=workspace_id
    )
    for i in template_list:
        url = url + i + "&shapes="
    response = client.delete(url[:-8], headers=client.token_headers)
    return response
