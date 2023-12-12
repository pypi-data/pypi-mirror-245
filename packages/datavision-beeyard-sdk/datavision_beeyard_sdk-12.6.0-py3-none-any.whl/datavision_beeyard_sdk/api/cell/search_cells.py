import json
from ...client import AuthenticatedClient


def query(
    *,
    client: AuthenticatedClient,
    query="",
    sort_by="created",
    sort_direction="desc",
    namespace="",
    page_index=0,
    page_size=100
):
    """Query existing cells.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.
    query : str, optional
        MongoDB query, by default "".
    sort_by : {'created', 'uploaded', 'modified'}, optional
        Sort results, by default "created".
    sort_direction : {'asc', 'desc'}, optional
        Sort results order, by default "asc"
    namespace : str, optional
        Search cells in specific namespace, by default all namespaces are searched.
    page_index : int, optional
        Return results from index page, by default 0.
    page_size : int, optional
        Number of cells per page, by default 100.

    Returns
    -------
    dict
        Results of the query.
    """
    url = "{}/api/v1/cells/search".format(client.base_url)
    url_with_param = (
        url
        + "?sortBy="
        + sort_by
        + "&sortDirection="
        + sort_direction
        + "&namespace="
        + namespace
        + "&pageIndex="
        + str(page_index)
        + "&pageSize="
        + str(page_size)
    )
    response = client.post(url_with_param, headers=client.token_headers, data=query)
    return json.loads(response.content.decode("utf-8"))
