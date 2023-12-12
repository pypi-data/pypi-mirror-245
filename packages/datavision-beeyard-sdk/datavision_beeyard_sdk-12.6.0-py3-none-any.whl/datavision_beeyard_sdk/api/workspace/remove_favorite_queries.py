from ...client import AuthenticatedClient


def delete(workspace_id: str, *, client: AuthenticatedClient, queries_list: [str]):
    """Remove favorite queries from workspace.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.
    queries_list : list[str]
        List of queries to be removed.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/workspaces/{workspaceId}/favoriteQueries?queries=".format(
        client.base_url, workspaceId=workspace_id
    )
    tmp = "&queries="
    for q in queries_list:
        url = url + q + tmp
    response = client.delete(url[: -len(tmp)], headers=client.token_headers)
    return response
