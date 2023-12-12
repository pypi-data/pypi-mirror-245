from ...client import AuthenticatedClient


def query(*, client: AuthenticatedClient, accept: str = "application/json", query="[]"):
    """Aggregate events.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.
    accept : str, optional
        mime type, by default "application/json".
    query : str, optional
        MongoDB query, by default "[]"

    Returns
    -------
    json string
        Content of the Http response from API as a json.
    """
    url = "{}/api/v1/events/aggregation".format(client.base_url)
    header = {k: v for k, v in client.token_headers.items()}
    header["accept"] = accept
    response = client.post(url, headers=header, data=query)
    return response.content
