from ...client import AuthenticatedClient
import json
from ...types import check_input


@check_input
def compute(
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    field: str,
    dataType: [str],
    query: str,
):
    """Aggregate files per workspace.

    Parameters
    ----------
    workspace_id : str
        Target workspace id.
    client : AuthenticatedClient
        BeeYard client.
    field : {'name', 'mimeType', 'dataType'}
        Aggregate files by `field`
    dataType : list[str]
        Each element must be one of ['image', 'document', 'overlay', 'file'] or an empty string.
    query : str
        MongoDB query.

    Returns
    -------
    dict
        Dictionary describing the cell.
    """
    url = "{}/api/v1/workspaces/{workspaceId}/cells/fileStats".format(
        client.base_url, workspaceId=workspace_id
    )
    url = url + f"?field={field}"
    for opt in dataType:
        if opt != "":
            url = url + f"&dataTypes={opt}"
    response = client.post(url, headers=client.token_headers, data=query)
    return json.loads(response.content)
