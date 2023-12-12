from ...client import AuthenticatedClient


def read(*, client: AuthenticatedClient, event_id: str):
    """Read events.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.
    event_id : str

    Returns
    -------
    json string
        Content of the Http response from API as a json.
    """
    url = "{}/api/v1/events/{eventId}".format(client.base_url, eventId=event_id)
    response = client.get(url, headers=client.token_headers)
    return response.content
