from ...client import AuthenticatedClient


def update(*, id: str, client: AuthenticatedClient, filename: str, json_body: str):
    """Modify file.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.
    filename : str
    json_body : json str
        New file content

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells/{id}/files/{filename}".format(
        client.base_url, id=id, filename=filename
    )
    header = {k: v for k, v in client.token_headers.items()}
    header["Content-Type"] = "application/json"
    response = client.patch(url, headers=header, data=json_body)
    return response
