import json
from ...client import AuthenticatedClient
from ...models.workspace_descriptor_dto import WorkspaceDescriptorDto


def create(*, client: AuthenticatedClient, request_body: WorkspaceDescriptorDto):
    """Create a new workspace.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.
    request_body : WorkspaceDescriptorDto
        Object containing name and namespace of the new workspace.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/workspaces".format(client.base_url)
    json_body = request_body.to_dict()
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    response = client.post(url, headers=header, data=json.dumps(json_body))
    return response
