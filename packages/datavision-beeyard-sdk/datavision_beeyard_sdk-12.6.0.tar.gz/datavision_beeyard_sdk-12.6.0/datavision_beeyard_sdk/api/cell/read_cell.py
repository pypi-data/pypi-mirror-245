from ...client import AuthenticatedClient
import json


def read(id: str, *, client: AuthenticatedClient):
    """Read cell.

    Parameters
    ----------
    id : str
        Id of the target cell.
    client : AuthenticatedClient
        BeeYard client.

    Returns
    -------
    dict
        Dictionary describing the cell.
    """
    url = "{}/api/v1/cells/{id}".format(client.base_url, id=id)
    response = client.get(url, headers=client.token_headers)
    return json.loads(response.content.decode("utf-8"))
