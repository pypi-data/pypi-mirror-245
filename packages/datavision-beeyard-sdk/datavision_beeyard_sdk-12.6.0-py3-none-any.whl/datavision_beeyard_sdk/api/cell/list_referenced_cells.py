from ...client import AuthenticatedClient
import json


def search(id: str, *, client: AuthenticatedClient):
    """List referenced cells.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    dict
        Dictionary containing the references.
    """
    url = "{}/api/v1/cells/{id}/references/cells".format(client.base_url, id=id)
    response = client.get(url, headers=client.token_headers)
    return json.loads(response.content)
